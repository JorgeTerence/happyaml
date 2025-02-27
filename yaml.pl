use warnings;
use strict;

package yaml;

# Aight I'm rolling a full on YAML parser in Perl. Perhaps the first of it's kind.
# We create a hashmap and add an entry an increment the indentation every time we see ':'
# TODO: hw to convert between $, @ and %

sub decode {
	my $FH;
	open(FH, '<', @_[0]);
	return yamler () 0 $FH;
}

sub yamler {
	my ($indent, $FH) = @_;
	my $line = <FH>;
	# Object or array
	if (/:$/m $line) {
		$indent += 2 # TODO: automatically detect indenting
		my $key = # remove whitespace
		return yamler {$key => ???} $indent $FH
	}
	# Single property or inline array
	else return #remove whitespace and convert to datatype
}
