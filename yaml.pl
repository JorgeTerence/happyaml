package yaml;

use warnings;
use strict;


# Aight I'm rolling a full on YAML parser in Perl. Perhaps the first of it's kind.
# We create a hashmap and add an entry an increment the indentation every time we see ':'
# TODO: ignore comments

sub gcd
{
    use integer;
    my($x, $y, $r);
    return 0 if (scalar @_ == 0);
    $y = abs pop @_;
    $x = abs pop @_;
    while (1)
    {
            ($x, $y) = ($y, $x) if ($y < $x);
            $r = $y % $x;
            $y = $x;
            if ($r == 0)
            {
                    return $x if (scalar @_ == 0);
                    $r = abs pop @_;
            }
            $x = $r;
    }
    return $y;
}

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
sub yamler { ##
    # @doc: string[] -> document lines
    # $indent_size: int -> indentation size for the whole document
    # $indent: int -> indentation for the current block
    # $i: int -> start position for the current block
    my (@doc, $indent_size, $indent, $i) = @_;
    my %obj;

    # foreach entry on the same indent level until there's one with less indentation (new parent object)
    foreach (@doc) {
        # breaks if the indent size is less than the current block
        if ((my $count = () = $_ =~ /\s{$indent_size}/) < $indent) { last; }

        my @matches = $_ =~ /\w+(?=:)/g;
        my $key = @matches[0];

        # if its an inline value, parse it and go to next, else call yamler again
        my @inline_values = $_ =~ /(?!:\s?)\S+$/g;
        print @inline_values;

        if (scalar @inline_values > 0) {
            # TODO: parse inline value types
            %obj{$key} = @inline_values;
        } else {
            my %val;
            %val = yamler(@doc, $indent_size, $indent + $indent_size, $i + 1);
            %obj{$key} = %val;
        }

        $i++;
    }
}

sub decode {
    my (@doc, $indentation) = read_lines pop;
	return yamler(@doc, $indentation, 0, 0);
}

1;
