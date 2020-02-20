#!/usr/bin/perl
#
if (scalar (@ARGV)<1){
	print "perl XXX 0 (to 9)\n";
	die;
}
srand($ARGV[0]);
#record train individual and testing individual
open REF, "../Demographic_survey.tsv" or die;
$tline=<REF>;
$tline=~s/"//g;
chomp $tline;
@title=split "\t", $tline;

while ($line=<REF>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	$pid="";
	$diagnosis="";
	foreach $aaa (@title){
		$value=shift @table;
		if ($aaa eq "healthCode"){
			$pid=$value;
		}
		if ($aaa eq "professional-diagnosis"){
			if ($value eq "true"){
				$value=1;
			}
			if ($value eq "false"){
				$value=0;
			}
			$diagnosis=$value;
		}
		$r=rand(1);
	}
		if (($diagnosis eq "1")||($diagnosis eq "0")){
			if ($r<0.5){
				#print TRAIN "$pid\t$diagnosis\n";
				$train_id{$pid}=$diagnosis;
			}else{
				#print TEST "$pid\t$diagnosis\n";
				$test_id{$pid}=$diagnosis;
			}
		}
}
close REF;
open FILE, "../Walking_activity_training.tsv" or die;
<FILE>;

#@all_train=keys %train_id;
#$n=scalar (@all_train);
#print "$n\n";
open TRAIN, ">train_gs.dat" or die;
open TEST, ">test_gs.dat" or die;
while ($line=<FILE>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	if (exists $train_id{$table[3]}){
		print TRAIN "$table[2]\t$train_id{$table[3]}\n";
	}
	if (exists $test_id{$table[3]}){
		print TEST "$table[2]\t$test_id{$table[3]}\n";
	}

}

close TRAIN;
close TEST;

	
