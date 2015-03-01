#!/usr/bin/perl
use strict;
use warnings;
my @t=("com", "net", "biz", "ru", "org", "co.uk", "info");
my $d; my $i; my $m; my $s; my $y;my $z;
if(scalar @ARGV !=3){
print "usage: perl dga-cryptolocker.pl $ARGV[0] d m y\n";
exit 0;
}
for($z=0; $z<100000; $z++){
$d = $ARGV[0];
$m = $ARGV[1];
$y = $ARGV[2] + $z;
$d *= 65537;
$m *= 65537;
$y *= 65537;
$s = $d>>3 ^ $y>>8 ^ $y>>11;
$s &= 3;
$s += 12;
my $n='';
for($i = 0; $i < $s; $i++){
$d = (($d<<13 & 0xFFFFFFFF)>>19 & 0xFFFFFFFF) ^ (($d>>1 & 0xFFFFFFFF)<<13 & 0xFFFFFFFF) ^ ($d>>19 & 0xFFFFFFFF); $d &= 0xFFFFFFFF;
$m = (($m<<2 & 0xFFFFFFFF)>>25 & 0xFFFFFFFF) ^ (($m>>3 & 0xFFFFFFFF)<<7 & 0xFFFFFFFF) ^ ($m>>25 & 0xFFFFFFFF); $m &= 0xFFFFFFFF;
$y = (($y<<3 & 0xFFFFFFFF)>>11 & 0xFFFFFFFF) ^ (($y>>4 & 0xFFFFFFFF)<<21 & 0xFFFFFFFF) ^ ($y>>11 & 0xFFFFFFFF); $y &= 0xFFFFFFFF;
$n.=chr(ord('a') + ($y ^ $m ^ $d) % 25);
}
my $domain=$n.'.'.$t[$z%7];
print "$domain\n";
}
