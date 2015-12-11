package Scripts;

import java.util.ArrayList;

public class Running {
	public static void main(String[] args) {
		System.out.println(minDis("abab", "aabb"));
	}
	public static int minDis(String a, String b){
		return Math.min(compute(a,b), compute(b,a));
		//return compute(a,b);
	}
	public static int compute(String a, String b) {
		int count = 0;
		char[] x = a.toCharArray();
		char[] y = b.toCharArray();
		int j= 0;
		ArrayList<String> deleted = new ArrayList<String>();
		int i = 0;
		for(i = 0; i < x.length && j < y.length; i++) {
			if(x[i] == y[j]) {
				j++;
				continue;
			}
			if(!b.contains(String.valueOf(x[i]))) {
				if(deleted.contains(String.valueOf(x[i]))) {
					deleted.remove(String.valueOf(x[i]));
				}
				count++; //insert				

			} else if (deleted.contains(String.valueOf(x[i]))) {
				deleted.remove(String.valueOf(x[i]));
				count++; //insert				
			} else {
				deleted.add(String.valueOf(y[j]));
				j++;
				count++; //delete;
				i--;
			}
		}
		count += (x.length - i); //insert
		return count;
		
	}
}
