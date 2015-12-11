package Scripts;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.Scanner;

public class GetGensimVectors {
	private static BufferedReader br;
	
	public static void main(String[] args) throws FileNotFoundException {
		br = new BufferedReader(new FileReader("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/sim_matrix.csv"));
		String currentLine;
		double[][] matrix = new double[3440][3440];
		try {
			int i = 0;
			int j;
			while ((currentLine = br.readLine()) != null) {
				Scanner s = new Scanner(currentLine);
				j =0;
				while(s.hasNext()) {
					double token = s.nextDouble();
					matrix[i][j] = token; j++;
				}
				i++;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		FileOutputStream out = new FileOutputStream("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/sim_matrix.data");
		try {
			ObjectOutputStream object = new ObjectOutputStream(out);
			object.writeObject(matrix);
			object.close();
			out.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
