// siRNArules 1.0

// This program predicts siRNA efficency - also see published paper Holen, RNA, 2006

// Note to user: it should be realized that it will add ACGT's from any text also... so text
// must be deleted before presented to the program

// The program starts by reading a file mRNA_input.dat containing the mRNA sequence

// Then it reads the file again and put all ACGTcount elements into
// an array seqArray (+1 element, also has the -1 end-of-file)

// Then all possible antisense strands are found and put into siRNA object

// In short, it reads any file, and converts it to sequence, and all antisense are found
// (theoretically n-23 possible, for a sequence of n nt. 

// The siRNA-objects are stored in a siRNA-array (siRNAlist).

// The next step is that each siRNA is evaluated 
// and thus given two quality numbers (PlusValue and NegValue) 

// Then sorted for the sum of PlusValue and NegValue

// Finally the sorted siRNAlist is printed to file output.dat,
// where the columns are the following: 
// a) The rank (out of all the possible siRNAs in the mRNA)
// b) original position in mRNA_input.dat 
// c) antisense sequence, 
// d) score of PlusValue (similarity to good siRNAs)
// e) score of NegValue (similarity to bad siRNAs)


// Program starts

// file-writing/reading tools are imported
import java.io.*;

public class siRNArules {
	public static void main(String[] arguments) {

		// ACGTcount is the global counter of sequence size
		int ACGTcount = 0;		
		// this is the global counter of siRNA & antisense strands	
		int numberOfAntisenseStrands = 0;
			
		// Here is the siRNA class definition				
		class siRNA {
		int original_mRNA_Position;
		int PlusValue;
		int NegValue;
		int antiSenseSeq[];
		
				

		}


// Here comes the section that reads the mRNA_input.dat file and counts the a,c,g,t -elements
// Note that only ACGTU and acgtu letters are counted.
		try{
			FileInputStream file = new
				FileInputStream("mRNA_input.dat");

			boolean eof = false;
			
			while (!eof) {
				int input = file.read();
								
				if (input == -1)
					eof = true;
				else 
				if (
				(input == 65) || (input ==67)
				||(input == 71) || (input ==84)
				||(input == 85) || (input ==97)				
				||(input == 99) || (input ==103)
				||(input == 116) || (input ==117)
				) ACGTcount++;
			}
			System.out.println("Counting file bytes...");
			System.out.println("File mRNA_input.dat contains " + ACGTcount + " ACGT elements, giving ");
			System.out.println((ACGTcount-22)+" possible siRNA objects.");

			// Here the number of siRNAs (and antisense strands) is defined
			numberOfAntisenseStrands = (ACGTcount-22);
			file.close();

		} catch (IOException e) {
			System.out.println("Error -- " + e.toString());
		}


// In this section the file is read again and the ACGTacgtUu are set into 
// an array, seqArray

		int[] seqArray = new int[ACGTcount+1];

		System.out.println("...putting elements into array...");
		try{
			FileInputStream file = new
				FileInputStream("mRNA_input.dat");
		
			boolean eof = false;
			
			int inputCount = 0;
			while (!eof) {
				int input = file.read();
				
				if (
				(input == 65) || (input ==67)
				||(input == 71) || (input ==84)
				||(input == 85) || (input ==97)				
				||(input == 99) || (input ==103)
				||(input == 116) || (input ==117)
				) seqArray[inputCount++]=input;
				
				if (input == -1)
					eof = true;
			
			}
			file.close();
			

		} catch (IOException e) {
			System.out.println("Error -- " + e.toString());

		}

// By now program contains an integer array, "seqArray" of a number, "ACGTcount", of letters (actually the ASCII-code for each letter)
// making possible the definition of number, "numberOfAntisensestrands", of siRNA-objects

// This section reads all antisense strands read into an array of siRNA objects, siRNAlist[]

// Also note that the position of each antisense-strand is defined from the 3' end
// (or the 5' end of the target sequence in the mRNA target.


		siRNA siRNAlist[] = new siRNA[numberOfAntisenseStrands];

		for (int tt = 0; tt < numberOfAntisenseStrands; tt++)
		{
			
			siRNAlist[tt] = new siRNA();
			siRNAlist[tt].antiSenseSeq = new int[21];
			siRNAlist[tt].original_mRNA_Position = (tt+1);

			for (int t = 0; t <= 20; t++) {


				// Finds antisense from sense sequence	
				siRNAlist[tt].antiSenseSeq[20-t] = seqArray[tt+t];

				// The letters are reduced to A, C, G and U (or actually the ASCII-code for these)

				// If position is A or a, then u is antisense
				if ((siRNAlist[tt].antiSenseSeq[20-t] == 65)||(siRNAlist[tt].antiSenseSeq[20-t] == 97))
					siRNAlist[tt].antiSenseSeq[20-t] = 85;
					
				//If position is C or c, then g is antisense
				else if ((siRNAlist[tt].antiSenseSeq[20-t] == 67)||(siRNAlist[tt].antiSenseSeq[20-t] == 99))
					siRNAlist[tt].antiSenseSeq[20-t] = 71;
					
				//If position is G or g, then c is antisense
				else if ((siRNAlist[tt].antiSenseSeq[20-t] == 71)||(siRNAlist[tt].antiSenseSeq[20-t] == 103))
					siRNAlist[tt].antiSenseSeq[20-t] = 67;
					
				//If position is T or t, then a is antisense
				else if ((siRNAlist[tt].antiSenseSeq[20-t] == 84)||(siRNAlist[tt].antiSenseSeq[20-t] == 116))
					siRNAlist[tt].antiSenseSeq[20-t] = 65;
					
				//If position is U or u, then a is antisense
				else if ((siRNAlist[tt].antiSenseSeq[20-t] == 85)||(siRNAlist[tt].antiSenseSeq[20-t] == 117))
					siRNAlist[tt].antiSenseSeq[20-t] = 65;
					
			}	
			
// Here comes the evaluation of each siRNA, the core of the program 

// It consider each position's letter (A, C, G, U) and modifies the parameter PlusValue
// of each siRNA.
			
			
			// Calculation of PlusValue
			// Position 1: A = 66, C = - 18,, G =-31, U = 78
			if (siRNAlist[tt].antiSenseSeq[0]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 66; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 67)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 85; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 31; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 78; 				
			
			// Pos 2 A = 20 G= -12 U = 40 
			if (siRNAlist[tt].antiSenseSeq[1]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 20; 				
			if (siRNAlist[tt].antiSenseSeq[1]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 12; 				
			if (siRNAlist[tt].antiSenseSeq[1]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 40; 				
			
			// Pos 3 A = 48 C = -8 G = -9 U = 2
			if (siRNAlist[tt].antiSenseSeq[2]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 48; 				
			if (siRNAlist[tt].antiSenseSeq[2]== 67)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 8; 				
			if (siRNAlist[tt].antiSenseSeq[2]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 9; 				
			if (siRNAlist[tt].antiSenseSeq[2]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 2; 				

			// Pos 5 U = 41
			if (siRNAlist[tt].antiSenseSeq[4]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 41; 				

 
			// Pos 6 A = 18, U = 18
			if (siRNAlist[tt].antiSenseSeq[5]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 18; 				
			if (siRNAlist[tt].antiSenseSeq[5]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 18; 				
			
			// Pos 7 A = 26, C = -13, G = -9, U = 38
			if (siRNAlist[tt].antiSenseSeq[6]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 26; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 67)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 13; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 9; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 38; 				

			// Pos 10 A = 54 G = - 22 U = -10
			if (siRNAlist[tt].antiSenseSeq[9]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 54; 				
			if (siRNAlist[tt].antiSenseSeq[9]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 22; 				
			if (siRNAlist[tt].antiSenseSeq[9]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 10; 				

			// Pos 11 A = 10, U = 29
			if (siRNAlist[tt].antiSenseSeq[10]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 10; 				
			if (siRNAlist[tt].antiSenseSeq[10]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 29; 				

			// Pos 14 A = 22, G = -12,  U = 22
			if (siRNAlist[tt].antiSenseSeq[13]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 22; 				
			if (siRNAlist[tt].antiSenseSeq[13]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 12; 				
			if (siRNAlist[tt].antiSenseSeq[13]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 22; 				

			// Pos 19 C = 31, G = 1
			if (siRNAlist[tt].antiSenseSeq[18]== 67)  
				siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 31; 				
			if (siRNAlist[tt].antiSenseSeq[18]== 71)  
				siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 1;

			
			// Pos 20 A = 16, U = 16
			if (siRNAlist[tt].antiSenseSeq[19]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 16; 				
			if (siRNAlist[tt].antiSenseSeq[19]== 85)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 16; 				

			// Pos 21 A = 16, C = -15, G = 28
			if (siRNAlist[tt].antiSenseSeq[20]== 65)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 16; 				
			if (siRNAlist[tt].antiSenseSeq[20]== 67)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue - 15; 				
			if (siRNAlist[tt].antiSenseSeq[20]== 71)  
				 siRNAlist[tt].PlusValue = siRNAlist[tt].PlusValue + 28; 				
	

			// Here comes the evaluation of the negative rules,
			// adding to the parameter NegValue of each siRNA
			
			// Position 1: A = -16, C = 59, G = 80, U = -32
			if (siRNAlist[tt].antiSenseSeq[0]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 16; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 59; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 80; 				
			if (siRNAlist[tt].antiSenseSeq[0]== 85)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 32; 				

			// Pos 2 A = -17, C = 53, G = 13, U = -16
			if (siRNAlist[tt].antiSenseSeq[1]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 17; 				
			if (siRNAlist[tt].antiSenseSeq[1]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 53; 				
			if (siRNAlist[tt].antiSenseSeq[1]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 13; 				
			if (siRNAlist[tt].antiSenseSeq[1]== 85)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 16;

			// Pos 4 C = 20, G = 34, U = -11
			if (siRNAlist[tt].antiSenseSeq[3]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 20; 				
			if (siRNAlist[tt].antiSenseSeq[3]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 34; 				
			if (siRNAlist[tt].antiSenseSeq[3]== 85)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 11;

			// Pos 5 A =15, C=15
			if (siRNAlist[tt].antiSenseSeq[4]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 15; 				
			if (siRNAlist[tt].antiSenseSeq[4]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 15;

			// Pos 6 A = 29
			if (siRNAlist[tt].antiSenseSeq[5]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 29; 				
 				
			// Pos 7 A = -10, C =52 G = 12 U = -11
			if (siRNAlist[tt].antiSenseSeq[6]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 10; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 52; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 12; 				
			if (siRNAlist[tt].antiSenseSeq[6]== 85)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 11; 				

			// Pos 10 A = -11 G = 8 U = 24
			if (siRNAlist[tt].antiSenseSeq[9]== 65)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 11; 				
			if (siRNAlist[tt].antiSenseSeq[9]== 71)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 8; 				
			if (siRNAlist[tt].antiSenseSeq[9]== 85)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 24;

			// Pos 11 A = -8 C = 38 G = 22 U = -13
			if (siRNAlist[tt].antiSenseSeq[10]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 8; 				
			if (siRNAlist[tt].antiSenseSeq[10]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 38; 				
			if (siRNAlist[tt].antiSenseSeq[10]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 22; 				
			if (siRNAlist[tt].antiSenseSeq[10]== 85)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 13; 				
	
			// Pos 13 A = -10 C = 20 G = 36
			if (siRNAlist[tt].antiSenseSeq[12]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 10; 				
			if (siRNAlist[tt].antiSenseSeq[12]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 20; 				
			if (siRNAlist[tt].antiSenseSeq[12]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 36; 				

			// Pos 14 C = 1 G =27
			if (siRNAlist[tt].antiSenseSeq[13]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 1; 				
			if (siRNAlist[tt].antiSenseSeq[13]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 27; 				

			// Pos 18 A = 37
			if (siRNAlist[tt].antiSenseSeq[17]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 37; 				

			// Pos 19 A = 80 C = -14 G = -11 U = -6
			if (siRNAlist[tt].antiSenseSeq[18]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 80; 				
			if (siRNAlist[tt].antiSenseSeq[18]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 14; 				
			if (siRNAlist[tt].antiSenseSeq[18]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 11; 				
			if (siRNAlist[tt].antiSenseSeq[18]== 85)  
				siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 6;

			// Pos 20 C = 28 G = 2
			if (siRNAlist[tt].antiSenseSeq[19]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 28; 				
			if (siRNAlist[tt].antiSenseSeq[19]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 2; 				
 				
			// Pos 21 A = 13 C = 31 G = -9
			if (siRNAlist[tt].antiSenseSeq[20]== 65)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 13; 				
			if (siRNAlist[tt].antiSenseSeq[20]== 67)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue + 31; 				
			if (siRNAlist[tt].antiSenseSeq[20]== 71)  
				 siRNAlist[tt].NegValue = siRNAlist[tt].NegValue - 9; 				

		// end-of-loop 	
		}


// At this point the program contains an array of siRNAs that have been evaluated
// according to rules for each position in their antisense sequence.

// Now comes the sorting of the array where two siRNAs are compared, and possibly 
// switched. More efficient sorting methods than this simple one exits.
// Rewriting this part should be considered if one has a very slow computer,
// or want to run comparisions on very large siRNA sets.

// For a switch, a new siRNA object, called siRNAswitch, carry the n+1
// element while n is becoming n+1, then siRNAswitch becomes n-element

   siRNA siRNAswitch = new siRNA();

   for (int nn = 0; nn < (numberOfAntisenseStrands-1); nn++)
	for (int n=0; n< (numberOfAntisenseStrands-1); n++)
		if ((siRNAlist[n].PlusValue - siRNAlist[n].NegValue) < (siRNAlist[n+1].PlusValue - siRNAlist[n+1].NegValue)) {
			siRNAswitch = siRNAlist[n];
			siRNAlist[n] = siRNAlist[n+1];
			siRNAlist[n+1] = siRNAswitch;
			}



	
// Finally, the siRNA-objects are printed to a file, one siRNA to a line with
// the following information 1) final ordered rank, 2) original position in mRNA
// 3) antisense sequence (5'-3'), 4) PosValue (similarity to set of best siRNAs)
// 5) NegValue (similarity to set of worst siRNAs)

		try {
 
                FileOutputStream f = new FileOutputStream("output.dat");
                PrintStream ps = new PrintStream( f );

 		// BufferedWriter bw = new BufferedWriter( new OutputStreamWriter( f ) );

                // This loop will print the file, one line per siRNA (& antisensestrand)

                for (int tt = 0; tt < numberOfAntisenseStrands; tt++) {
 
                    ps.print( (tt +1) );
                    ps.print( "\t" );

                    ps.print( siRNAlist[tt].original_mRNA_Position );
                    ps.print( "\t" );
                    for ( int i = 0; i <= 20; i++ )
                        ps.print( (char)siRNAlist[tt].antiSenseSeq[i] );
                    ps.print( "\t" );
                    ps.print( siRNAlist[tt].PlusValue );
                    ps.print( "\t" );
                    ps.print( siRNAlist[tt].NegValue );
		    ps.print( "\r");
		    ps.print( "\n");

                    
                }
                    ps.close();
                    System.out.println("File output.dat written with antisense seq and sorted to sum of Pos and Neg Values.");
 
                } catch (IOException e) {
                    System.out.println("Error - " + e.toString());
                }
 

	}
}