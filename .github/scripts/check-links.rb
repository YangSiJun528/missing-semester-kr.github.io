#!/usr/bin/env ruby
# frozen_string_literal: true

require "html-proofer"
require "yaml"
require "uri"

config = YAML.safe_load(File.read(File.expand_path("../link-check.yml", __dir__)))
ignore_urls = config.fetch("ignore_urls") +
  config.fetch("ignore_url_patterns").map { |pattern| Regexp.new(pattern) }

options = {
  checks: ["Links", "Scripts", "Images", "Favicon", "OpenGraph"],
  cache: { timeframe: { internal: "1d", external: "1d" } },
  check_external_hash: true,
  ignore_empty_alt: false,
  ignore_missing_alt: false,
  allow_missing_href: false,
  enforce_https: false,
  hydra: { max_concurrency: 10 },
  typhoeus: {
    cookiefile: ".cookies",
    cookiejar: ".cookies",
    connecttimeout: 30,
    timeout: 120,
    followlocation: true,
    # Negotiate and decode compression so incomplete uncompressed bodies do not fail anchor checks.
    accept_encoding: "",
    headers: {
      "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.0.0 Safari/537.36",
    },
  },
  ignore_urls: ignore_urls,
  swap_urls: config.fetch("swap_urls").transform_keys { |pattern| Regexp.new(pattern) },
}

begin
  proofer = HTMLProofer.check_directory(ARGV.fetch(0, "_site"), options)
  token = ENV.fetch("GITHUB_TOKEN", "")
  proofer.before_request do |request|
    uri = URI.parse(request.url)
    if uri.scheme == "https" && uri.host == "github.com" && !token.empty?
      request.options[:headers] = request.options[:headers].merge("Authorization" => "Bearer #{token}")
    end
  end
  proofer.run
rescue StandardError => error
  warn error.message
  exit 1
end
