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


#@mat=glob("eva.txt*test");

$file_i=1;
@total=();
@total_c=();
while ($file_i<6){
	open PRED, "fold_${fold}/outbound/eva.txt.${file_i}.test" or die;
	open GS, "test_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref[$file_i]{$map{$table_gs[0]}}+=$table[1];
			$ref_count[$file_i]{$map{$table_gs[0]}}++;
			$total[$file_i]+=$table[1];
			$total_c[$file_i]++;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}
$file_i=1;
while ($file_i<6){
	$avg[$file_i]=$total[$file_i]/$total_c[$file_i];
	$file_i++;
}



$file_i=1;
@total_rest=();
@total_c_rest=();
while ($file_i<6){
	open PRED, "fold_${fold}/rest/eva.txt.${file_i}.test" or die;
	open GS, "test_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_rest[$file_i]{$map{$table_gs[0]}}+=$table[1];
			$ref_rest_count[$file_i]{$map{$table_gs[0]}}++;
			$total_rest[$file_i]+=$table[1];
			$total_c_rest[$file_i]++;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}
$file_i=1;
while ($file_i<6){
	$avg_rest[$file_i]=$total_rest[$file_i]/$total_c_rest[$file_i];
	$file_i++;
}

$file_i=1;
@total_return=();
@total_c_return=();
while ($file_i<6){
	open PRED, "fold_${fold}/return/eva.txt.${file_i}.test" or die;
	open GS, "test_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_return[$file_i]{$map{$table_gs[0]}}+=$table[1];
			$ref_return_count[$file_i]{$map{$table_gs[0]}}++;
			$total_return[$file_i]+=$table[1];
			$total_c_return[$file_i]++;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}
$file_i=1;
while ($file_i<6){
	$avg_return[$file_i]=$total_return[$file_i]/$total_c_return[$file_i];
	$file_i++;
}












open FINAL, ">feature_test.txt" or die;
open FILE, "test_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]";

	$file_i=1;
	while ($file_i<6){
		if ($ref[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg[$file_i]";
		}else{
			$val=$ref[$file_i]{$map{$table[0]}}/$ref_count[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$file_i=1;
	while ($file_i<6){
		if ($ref_rest[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg_rest[$file_i]";
		}else{
			$val=$ref_rest[$file_i]{$map{$table[0]}}/$ref_rest_count[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}

	$file_i=1;
	while ($file_i<6){
		if ($ref_return[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg_return[$file_i]";
		}else{
			$val=$ref_return[$file_i]{$map{$table[0]}}/$ref_return_count[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}








	print FINAL "\n";
	$i++;
}
close FINAL;
close FILE;

