use strict;
use warnings;

require "./yaml.pm";
my $spec = decode("openapi.yaml");
print (my @matches = ("      name: Jorge" =~ /\w+(?=:)/g));
