package Scripts;
import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;
import edu.cmu.lti.lexical_db.ILexicalDatabase;
import edu.cmu.lti.lexical_db.NictWordNet;
import edu.cmu.lti.ws4j.RelatednessCalculator;
import edu.cmu.lti.ws4j.impl.HirstStOnge;
import edu.cmu.lti.ws4j.impl.JiangConrath;
import edu.cmu.lti.ws4j.impl.LeacockChodorow;
import edu.cmu.lti.ws4j.impl.Lesk;
import edu.cmu.lti.ws4j.impl.Lin;
import edu.cmu.lti.ws4j.impl.Path;
import edu.cmu.lti.ws4j.impl.Resnik;
import edu.cmu.lti.ws4j.impl.WuPalmer;
import edu.cmu.lti.ws4j.util.WS4JConfiguration;


public class GetVerbs {
	private static BufferedReader bufferedReader;
	private static ILexicalDatabase db = new NictWordNet();
	
	//computes matrix based on what metric you give it
	private static double[][] compute(String[] word1, String[] word2, String metric) {
		System.out.println("computing matrix");
		WS4JConfiguration.getInstance().setMFS(true);
		double[][] matrix;
		switch(metric) {
		case "HirstStOnge":
			matrix = (new HirstStOnge(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;				
		case "LeacockChodorow":
		matrix = (new LeacockChodorow(db).getNormalizedSimilarityMatrix(word1, word2));
		return matrix;
		case "Lesk":
			matrix = (new Lesk(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;				
		case "WuPalmer":
			System.out.println("WuPalmer");
			matrix = (new WuPalmer(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;				
		case "Resnik":
			matrix = (new Resnik(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;
		case "JiangConrath":
			matrix = (new JiangConrath(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;
		case "Lin":
			matrix = (new Lin(db).getNormalizedSimilarityMatrix(word1, word2));
			return matrix;
		}
		return null;
	}
 
	public static void main(String[] args) throws IOException{
		List<String> verbList = new ArrayList<String>();
		bufferedReader = new BufferedReader(new FileReader("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/verbsInCorpus.txt"));
		String currentLine;
		while((currentLine = bufferedReader.readLine() )!= null) {
			verbList.add(currentLine);
		}
		//get array of all verbs
		String[] verbArray = verbList.toArray(new String[verbList.size()]);
		System.out.println(verbList.toString());
		//String[] verbArray = {"run", "jump", "hide", "eat", "play"};
		//compute normalized similarity score matrix
		double[][] matrixWUP = compute(verbArray,verbArray, "WuPalmer");
		
		//normalize matrix
		
		//Write matrix to disk with FileOutputStream
		System.out.println("saving");
        FileOutputStream f_out = new FileOutputStream("/Users/meerahahn/Desktop/Development/NLP_Research/wordNetData/WuPalmer.data");

        // Write object with ObjectOutputStream
        ObjectOutputStream obj_out = new ObjectOutputStream (f_out);

        // Write object out to disk
        obj_out.writeObject(matrixWUP);
        obj_out.close();
	}
}
