#!/usr/bin/perl
#
$fold=$ARGV[0];
@mat=glob("fold_${fold}/outbound/eva.txt*train");
@total=();
@total_c=();
$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/outbound/eva.txt.${file_i}.train" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref[$file_i][$i]=$table[1];
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

@mat=glob("fold_${fold}/rest/eva.txt*train");
@total_rest=();
@total_c_rest=();
$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/rest/eva.txt.${file_i}.train" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref_rest[$file_i][$i]=$table[1];
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


@mat=glob("fold_${fold}/return/eva.txt*train");
@total_return=();
@total_c_return=();
$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/return/eva.txt.${file_i}.train" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		if ($table[1] eq ""){}else{
			$ref_return[$file_i][$i]=$table[1];
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




open FINAL, ">feature_train.txt" or die;
open FILE, "train_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]";
	$file_i=1;
	while ($file_i<6){
		if ($ref[$file_i][$i] eq ""){
			print FINAL "\t$avg[$file_i]";
		}else{
			$val=$ref[$file_i][$i];
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$file_i=1;
	while ($file_i<6){
		if ($ref_rest[$file_i][$i] eq ""){
			print FINAL "\t$avg_rest[$file_i]";
		}else{
			$val=$ref_rest[$file_i][$i];
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$file_i=1;
	while ($file_i<6){
		if ($ref_return[$file_i][$i] eq ""){
			print FINAL "\t$avg_return[$file_i]";
		}else{
			$val=$ref_return[$file_i][$i];
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$i++;
	print FINAL "\n";
}
close FINAL;
close FILE;

