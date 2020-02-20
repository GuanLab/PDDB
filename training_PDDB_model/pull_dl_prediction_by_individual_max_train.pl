#!/usr/bin/perl
#
## map all records to individual;
## for each individual, let us pick up the maximal predictions

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
			$ref{$table_gs[0]}+=$table[1];
			$ref_count{$table_gs[0]}++;
#			$total+=$table[1];
#			$total_c++;
		}
		$i++;
	}
	close PRED;
	$total_file++;
}




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
			$ref_rest{$table_gs[0]}+=$table[1];
			$ref_rest_count{$table_gs[0]}++;
#			$total+=$table[1];
#			$total_c++;
		}
		$i++;
	}
	close PRED;
	$total_file_rest++;
}



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
			$ref_return{$table_gs[0]}+=$table[1];
			$ref_return_count{$table_gs[0]}++;
#			$total+=$table[1];
#			$total_c++;
		}
		$i++;
	}
	close PRED;
	$total_file_return++;
}






#$avg=$total/$total_c;



#$avg=$total/$total_c;

@all_record=keys %ref;
foreach $record (@all_record){
	if ($ref{$record}>$ref_map{$map{$record}}){
		$ref_map{$map{$record}}=$ref{$record};
	}
}
foreach $record (@all_record){
	if ($ref{$record} eq ""){}else{
		$total+=$ref{$record};
		$total_c++;
	}
}



@all_record_rest=keys %ref_rest;
foreach $record (@all_record_rest){
	if ($ref_rest{$record}>$ref_map_rest{$map{$record}}){
		$ref_map_rest{$map{$record}}=$ref_rest{$record};
	}
}
foreach $record (@all_record_rest){
	if ($ref_rest{$record} eq ""){}else{
		$total_rest+=$ref_rest{$record};
		$total_c_rest++;
	}
}


@all_record_return=keys %ref_return;
foreach $record (@all_record_return){
	if ($ref_return{$record}>$ref_map_return{$map{$record}}){
		$ref_map_return{$map{$record}}=$ref_return{$record};
	}
}
foreach $record (@all_record_return){
	if ($ref_return{$record} eq ""){}else{
		$total_return+=$ref_return{$record};
		$total_c_return++;
	}
}



$avg=$total/$total_c;
$avg_rest=$total_rest/$total_c_rest;
$avg_return=$total_return/$total_c_return;

open FINAL, ">feature_train.txt" or die;
open FILE, "train_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]\t";

	if ($ref_map{$map{$table[0]}} eq ""){
		print FINAL "$avg";
	}else{
		$val=$ref_map{$map{$table[0]}};
		print FINAL "$val";
	}

	if ($ref_map_rest{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_rest";
	}else{
		$val=$ref_map_rest{$map{$table[0]}};
		print FINAL "\t$val";
	}

	if ($ref_map_return{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_return";
	}else{
		$val=$ref_map_return{$map{$table[0]}};
		print FINAL "\t$val";
	}

	print FINAL "\n";
	$i++;
}
close FINAL;
close FILE;






$avg=$total/$total_c/5;
$avg_rest=$total_rest/$total_c_rest/5;
$avg_return=$total_return/$total_c_return/5;

open FINAL, ">feature_train.txt" or die;
open FILE, "train_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]\t";
	if ($ref_map{$map{$table[0]}} eq ""){
		print FINAL "$avg";
	}else{
		$val=$ref_map{$map{$table[0]}}/5;
		print FINAL "$val";
	}

	if ($ref_map_rest{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_rest";
	}else{
		$val=$ref_map_rest{$map{$table[0]}}/5;
		print FINAL "\t$val";
	}


	if ($ref_map_return{$map{$table[0]}} eq ""){
		print FINAL "\t$avg_return";
	}else{
		$val=$ref_map_return{$map{$table[0]}}/5;
		print FINAL "\t$val";
	}


	print FINAL "\n";

	$i++;
}
close FINAL;
close FILE;

