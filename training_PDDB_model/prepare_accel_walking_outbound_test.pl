#!/usr/bin/perl
#
## record deviceMotion column
open REF, "../Walking_activity_training.tsv" or die;
while ($line=<REF>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	$rid=$table[2];
	$accel_walking_out=$table[7];
	if ($accel_walking_out eq ""){}else{
		$record{$rid}=$accel_walking_out;
	}
}
close REF;

open OLD, "test_gs.dat" or die;
open NEW, ">deviceMotion_outbound_test.txt" or die;
while ($line=<OLD>){
	chomp $line;
	@table=split "\t", $line;
	if (-e "../outbound/$record{$table[0]}"){
		print NEW "$table[1]\t../outbound/$record{$table[0]}\n";
	}else{
		print NEW "$table[1]\t\n";
	}

}

