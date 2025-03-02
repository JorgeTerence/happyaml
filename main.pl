use strict;
use warnings;

# print my $c = () = '    hello: "main"' =~ /\s{2}/g

require "./yaml.pl";
my $spec = yaml::decode("openapi.yaml");
