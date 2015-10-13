#!/usr/bin/perl

@Path=qw(
blackscholes
bodytrack
canneal
dedup
facesim
ferret
fluidanimate
freqmine
rtview
streamcluster
swaptions
vips
x264
);

@Size=qw(
64
128
192
);

@Size2=qw(
4
6
20
);


$Output="Result";
mkdir "$Output";
open(FILE_SUM, ">", "$Output/stats."."out.txt") or die "Cannot open Overall.\n";
printf FILE_SUM ("Bench\tSize\tAppend\tSim_Sec\tSim_Ins\tHost_Sec\tDcache_Access\tDcache_MissRate\tIcache_Access\tIcache_MissRate\n");

@e1 = 1;
@e2 = 8;
$p = 0;
@array = ();
foreach $Path (@Path)
{
   foreach $Size (@Size){
	   #foreach $Size2 (@Size2){
#    print "Stage 1: $Bench.\n";
		#	printf "$tag |\n";
			$s = 0;
      		open(FILE, "Yue\_Parsec\_"."$Size"."MB/"."$Path"."/stats.txt") or print "Cannot open the benchmark "."Yue\_Parse\_"."$Size"."M/"."$Path"."/stats.txt\n";
		foreach $line (<FILE>){
			#print "$tag 0 $line";

			if($line =~ /Begin Simulation Statistics/)
			{
				#printf FILE_SUM ("%8s\_$p",$Path);
               @bs =();
               @bb = ();
               $ss = 0;
               $hs = 0;
               $si = 0;
               $da = 0;
               $dr = 0;
               $ia = 0;
               $ir = 0;
               $i = 0;
               $j = 0;
                $s++;
			}
            #else
            if($line =~ /sim_seconds/)
            {
               @array=split(/ +/,$line);
               $ss = 0 + @array[1]; 
            }
            if($line =~ /host_seconds/)
            {
               @array=split(/ +/,$line);
               $hs = 0 + @array[1]; 
            }            
            if($line =~ /sim_insts/)
            {
               @array=split(/ +/,$line);
               $si = 0 + @array[1]; 
            }
            if($line =~ /system.l2.overall_accesses::total/)
            {
               @array=split(/ +/,$line);
               $da = 0 + @array[1]; 
            }
            if($line =~ /system.l2.overall_miss_rate::total/)
            {
               @array=split(/ +/,$line);
               $dr = 0 + @array[1]; 
            }
            if($line =~ /system.l2.overall_accesses::total/)
            {
               @array=split(/ +/,$line);
               $ia = 0 + @array[1]; 
            }
            if($line =~ /system.l2.overall_miss_rate::total/)
            {
               @array=split(/ +/,$line);
               $ir = 0 + @array[1]; 
            }
            if($line =~ /End Simulation Statistics/)
			{
				if($s == 3)
				{
               printf FILE_SUM ("$Path\t$Size"."MB\t");
                printf FILE_SUM ("$ss\t");
                printf FILE_SUM ("$si\t");
                printf FILE_SUM ("$hs\t");
                printf FILE_SUM ("$da\t");
                printf FILE_SUM ("$dr\t");
                printf FILE_SUM ("$ia\t");
                printf FILE_SUM ("$ir\n");
				#printf FILE_SUM ("busyDetail");
                #foreach $bb (@bb)
                #{
                #  printf FILE_SUM ("\t$bb");
                #}
                #printf FILE_SUM ("\n"); 
                #printf FILE_SUM ("serveDetail");    
                #foreach $bs (@bs)
                #{
                #  printf FILE_SUM ("\t$bs");
                #}
				#printf FILE_SUM ("\n");
            }

				#print ("$s\n");
			}      
    }
		#finish foreach $linea

		close (FILE);
		#}
	}
}
	

close (FILE_SUM);
