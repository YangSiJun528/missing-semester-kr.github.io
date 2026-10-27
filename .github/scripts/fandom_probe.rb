require "json"
require "open3"
require "tmpdir"
require "fileutils"
require "time"
require "digest"

URLS = [
  "https://vim.fandom.com/wiki/Search_and_replace",
  "https://vim.fandom.com/wiki/Map_caps_lock_to_escape_in_macOS",
  "https://vim.fandom.com/wiki/Using_undo_branches#Persistent_undo",
  "https://vim.fandom.com/wiki/Vim_Tips_Wiki",
  "https://vim.fandom.com/wiki/Vim_key_bindings_for_web_browsers",
].freeze
ACTION_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.0.0 Safari/537.36"
ENVIRONMENT = ENV.fetch("PROBE_ENV", "local")
OUTPUT = File.expand_path("diagnostics/#{ENVIRONMENT}")
FileUtils.mkdir_p(OUTPUT)

def probe(label, url, method: "GET", user_agent: ACTION_UA, browser_headers: false)
  started = Time.now.utc.iso8601(6)
  Dir.mktmpdir("fandom-probe-") do |dir|
    headers = File.join(dir, "headers")
    body = File.join(dir, "body")
    command = ["curl", "--silent", "--show-error", "--location", "--connect-timeout", "30", "--max-time", "120",
               "--dump-header", headers, "--output", body, "--write-out", "%{json}"]
    command += ["--user-agent", user_agent] if user_agent
    command << "--head" if method == "HEAD"
    if browser_headers
      command += ["--header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "--header", "Accept-Language: en-US,en;q=0.9"]
    end
    command << url
    stdout, stderr, status = Open3.capture3(*command)
    metrics = JSON.parse(stdout) rescue { "parse_error" => stdout }
    keys = %w[http_code http_version url_effective num_redirects remote_ip remote_port time_namelookup time_connect time_appconnect time_pretransfer time_starttransfer time_redirect time_total size_download ssl_verify_result exitcode errormsg]
    metrics = metrics.select { |key, _| keys.include?(key) }
    raw_headers = File.exist?(headers) ? File.read(headers, encoding: "UTF-8", invalid: :replace, undef: :replace) : ""
    safe_headers = raw_headers.lines.map { |line| line.match?(/\Aset-cookie:/i) ? "Set-Cookie: [redacted]\n" : line }.join
    raw_body = File.exist?(body) && method != "HEAD" ? File.binread(body) : ""
    text = raw_body.encode("UTF-8", invalid: :replace, undef: :replace)
    title = text[/<title[^>]*>(.*?)<\/title>/im, 1]
    record = { environment: ENVIRONMENT, label: label, url: url, method: method, user_agent: user_agent || "curl default",
               browser_headers: browser_headers, started_at: started, exit_code: status.exitstatus,
               stderr: stderr, metrics: metrics, response_headers: safe_headers, title: title,
               body_sha256: Digest::SHA256.hexdigest(raw_body), body_bytes: raw_body.bytesize }
    File.write(File.join(OUTPUT, "#{label}.json"), JSON.pretty_generate(record) + "\n")
    File.write(File.join(OUTPUT, "#{label}.headers.txt"), safe_headers)
    File.binwrite(File.join(OUTPUT, "#{label}.body-prefix.txt"), raw_body.byteslice(0, 16_384)) unless raw_body.empty?
    puts JSON.generate(record.reject { |key, _| key == :response_headers })
    record
  end
end

metadata = { environment: ENVIRONMENT, ruby: RUBY_DESCRIPTION, curl: Open3.capture3("curl", "--version").first,
             uname: Open3.capture3("uname", "-a").first, proxy_variable_names: ENV.keys.grep(/\A(?:http|https|all|no)_proxy\z/i),
             head_sha: ENV["GITHUB_SHA"], started_at: Time.now.utc.iso8601 }
File.write(File.join(OUTPUT, "environment.json"), JSON.pretty_generate(metadata) + "\n")

# The first requests target only one article, before the five-URL comparison.
records = []
records << probe("single-head", URLS.first, method: "HEAD")
records << probe("single-get", URLS.first)
records << probe("single-default-ua", URLS.first, user_agent: nil)
records << probe("single-browser-headers", URLS.first, browser_headers: true)

URLS.each_with_index do |url, index|
  records << probe("serial-#{index}", url)
  sleep 1
end
threads = URLS.each_with_index.map do |url, index|
  Thread.new { probe("parallel-#{index}", url) }
end
records.concat(threads.map(&:value))
File.write(File.join(OUTPUT, "results.json"), JSON.pretty_generate(records) + "\n")

# Collection is useful even on failure, but a rejected URL is not a passing check.
exit(records.all? { |row| row[:exit_code] == 0 && (row[:metrics]["http_code"] || 0).between?(200, 299) } ? 0 : 1)
