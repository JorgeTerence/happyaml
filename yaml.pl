package yaml;

use warnings;
use strict;
use Math::Utils qw(:utility);


# Aight I'm rolling a full on YAML parser in Perl. Perhaps the first of it's kind.
# We create a hashmap and add an entry an increment the indentation every time we see ':'
# TODO: ignore comments

sub read_lines {
	my ($FH, @lines, @indents);

	open FH, '<', pop;

    while (<FH>) {
        push @lines, $_;
        push @indents, length $_ =~ /^\s+/;
    }

    return @lines, gcd @indents;
}

### -> %obj
sub yamler {
    # @doc: string[] -> document lines
    # $indent_size: int -> indentation size for the whole document
    # $indent: int -> indentation for the current block
    # $i: int -> start position for the current block
    my ($doc_ref, $indent_size, $indent, $i) = $_;
    my %obj;

    # foreach entry on the same indent level until there's one with less indentation (new parent object)
    foreach (@$doc_ref) {
        # print $_;
        # breaks if the indent size is less than the current block
        if (scalar (my $count = () = $_ =~ /\s{$indent_size}/) < $indent) { last; }

        my @matches = $_ =~ /\w+(?=:)/g;
        my $key = $matches[0];

        # if its an inline value, parse it and go to next, else call yamler again
        my @inline_values = $_ =~ /(?!:\s?)\S+$/g;
        if (scalar @inline_values > 0) {
            # TODO: parse inline value types
            # %obj{$key} = @inline_values;
        } else {
            my %val;
            # %val = yamler($doc_ref, $indent_size, $indent + $indent_size, $i + 1);
            # %obj{$key} = %val;
        }

        $i++;
    }
}

sub decode {
    my (@doc, $indentation) = read_lines pop;
	return yamler \@doc, $indentation, 0, 0;
}

1;
