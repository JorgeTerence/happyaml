use strict;
use warnings;
use yaml;

package main;

my $spec = yaml::decode(@ARGV[0])
