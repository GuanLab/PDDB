#!/usr/bin/perl
#
## record deviceMotion column
open REF, "../Walking_activity_training.tsv" or die;
while ($line=<REF>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	$rid=$table[2];
	$accel_walking_rest=$table[13];
	if ($accel_walking_rest eq ""){}else{
		$record{$rid}=$accel_walking_rest;
	}
}
close REF;

open OLD, "test_gs.dat" or die;
open NEW, ">accl_rest_test.txt" or die;
while ($line=<OLD>){
	chomp $line;
	@table=split "\t", $line;
	if (-e "../rest/$record{$table[0]}.npy"){
		print NEW "$table[1]\t../rest/$record{$table[0]}.npy\n";
	}else{
		print NEW "$table[1]\t\n";
	}

}

