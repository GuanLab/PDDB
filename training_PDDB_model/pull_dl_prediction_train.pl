#!/usr/bin/perl
#
$fold=$ARGV[0];
@mat=glob("fold_${fold}/outbound/eva.txt*train");
$total_file=0;
$total=0;
$total_c=0;
foreach $eva (@mat){
	open PRED, $eva or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref[$i]+=$table[1];
			$ref_count[$i]++;
			$total+=$table[1];
			$total_c++;
		}
		$i++;
	}
	close PRED;
	$total_file++;
}
$avg=$total/$total_c;


@mat=glob("fold_${fold}/rest/eva.txt*train");
$total_file_rest=0;
$total_rest=0;
$total_c_rest=0;
foreach $eva (@mat){
	open PRED, $eva or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref_rest[$i]+=$table[1];
			$ref_rest_count[$i]++;
			$total_rest+=$table[1];
			$total_c_rest++;
		}
		$i++;
	}
	close PRED;
	$total_file_rest++;
}

$avg_rest=$total_rest/$total_c_rest;


@mat=glob("fold_${fold}/return/eva.txt*train");
$total_file_return=0;
$total_return=0;
$total_c_return=0;
foreach $eva (@mat){
	open PRED, $eva or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref_return[$i]+=$table[1];
			$ref_return_count[$i]++;
			$total_return+=$table[1];
			$total_c_return++;
		}
		$i++;
	}
	close PRED;
	$total_file_return++;
}

$avg_return=$total_return/$total_c_return;



open FINAL, ">feature_train.txt" or die;
open FILE, "train_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]\t";

	if ($ref[$i] eq ""){
		print FINAL "$avg";
	}else{
		$val=$ref[$i]/$ref_count[$i];
		print FINAL "$val";
	}

	if ($ref_rest[$i] eq ""){
		print FINAL "\t$avg_rest";
	}else{
		$val=$ref_rest[$i]/$ref_rest_count[$i];
		print FINAL "\t$val";
	}

	if ($ref_return[$i] eq ""){
		print FINAL "\t$avg_return";
	}else{
		$val=$ref_return[$i]/$ref_return_count[$i];
		print FINAL "\t$val";
	}


	print FINAL "\n";
	$i++;
}
close FINAL;
close FILE;

