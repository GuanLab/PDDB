#!/usr/bin/perl
#
## map all records to individual;

$fold=$ARGV[0];

open MAP, "../../full_train_data/Walking_activity_training.tsv" or die;
<MAP>;
while ($line=<MAP>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	$map{$table[2]}=$table[3];
}
close MAP;


@mat=glob("fold_${fold}/outbound/eva.txt*train");
$total_file=0;
$total=0;
$total_c=0;
foreach $eva (@mat){
	open PRED, $eva or die;
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref{$map{$table_gs[0]}}+=$table[1];
			$total+=$table[1];
			$total_count{$map{$table_gs[0]}}++;
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
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_rest{$map{$table_gs[0]}}+=$table[1];
			$total_rest+=$table[1];
			$total_count_rest{$map{$table_gs[0]}}++;
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
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_return{$map{$table_gs[0]}}+=$table[1];
			$total_return+=$table[1];
			$total_count_return{$map{$table_gs[0]}}++;
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
	if ($ref{$map{$table[0]}} eq ""){
		print FINAL "$avg";
	}else{
		$val=$ref{$map{$table[0]}}/$total_count{$map{$table[0]}};
		print FINAL "$val";
	}

	if ($ref_rest{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_rest";
	}else{
		$val=$ref_rest{$map{$table[0]}}/$total_count_rest{$map{$table[0]}};
		print FINAL "\t$val";
	}

	if ($ref_return{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_return\n";
	}else{
		$val=$ref_return{$map{$table[0]}}/$total_count_return{$map{$table[0]}};
		print FINAL "\t$val\n";
	}




	$i++;
}
close FINAL;
close FILE;

