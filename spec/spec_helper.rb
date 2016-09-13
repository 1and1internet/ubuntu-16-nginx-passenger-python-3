require 'rspec'
require 'serverspec'
require 'docker'
require_relative '../../drone-tests/shared/jemonkeypatch.rb'

LISTEN_PORT=8080

base_spec_dir = Pathname.new(File.join(File.dirname(__FILE__)))
Dir[base_spec_dir.join('../../drone-tests/shared/**/*.rb')].sort.each { |f| require_relative f }

set :backend, :docker
@image = Docker::Image.get(ENV['IMAGE'])
set :docker_image, @image.id
#set :docker_debug, true
set :docker_container_start_timeout, 240
set :docker_container_ready_regex, /Zend Framework 2 should be installed/

set :docker_container_create_options, {
  'Image'      => @image.id,
  'User'       => '100000'
}

RSpec.configure do |c|

  describe "tests" do
    include_examples 'docker-ubuntu-16'
    include_examples 'docker-ubuntu-16-nginx-1.10.0'
    include_examples 'passenger-5-tests'
    include_examples 'python-3-tests'
  end
end
