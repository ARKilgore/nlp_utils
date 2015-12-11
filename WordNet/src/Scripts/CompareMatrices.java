package Scripts;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;

public class CompareMatrices {
	public static void main(String[] args) {
		double[][] matrix1;
		double[][] matrix2;
		try {
			FileInputStream fin = new FileInputStream("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/sim_matrix.data");
			ObjectInputStream objin = new ObjectInputStream(fin);
			matrix1 = (double[][]) objin.readObject();
			fin = new FileInputStream("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/matrix.data");
			objin = new ObjectInputStream(fin);
			matrix2 = (double[][]) objin.readObject();
			double sum = 0; 
			for(int i = 0; i < matrix1.length && i < matrix2.length; i++) {
				for(int j = 0; j < matrix1.length && j < matrix2.length; j ++) {
					sum += Math.pow(matrix2[i][j] - matrix1[i][j], 2);
				}
			}
			System.out.println(sum);
		} catch (IOException | ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
