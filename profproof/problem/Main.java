import java.util.Scanner;
import java.lang.Math;

public class Main {
	public static void main(String[] args) {
		readInput();
	}

	public static void test() {
		System.out.printf("The maximum product is %d.\n", result(new int[]{-2, 2, -2, -2}));
	}

	public static void readInput() {
		Scanner sin = new Scanner(System.in);
		int M = 0;
		while (sin.hasNextInt()) {
			M++;
			int N = sin.nextInt();
			int[] list = new int[N];
			for (int i = 0; i < N; ++i) {
				list[i] = sin.nextInt();
			}
			System.out.printf("Case #%d: The maximum product is %d.\n\n", M, result(list));
		}
		sin.close();
	}

	public static long result(int[] list) {
		long maxProd = 0;
		int N = list.length;
		for (int i = 1; i <= N; ++i) {
			for (int j = 0; j < N - i + 1; ++j) {
				//System.out.printf("%d elements starting from %d\n", i, j);
				long prod = 1;
				for (int k = j; k < i + j; ++k) {
					//System.out.printf("%d: %d to %d\n", k, j, i + j);
					prod *= list[k];
				}
				maxProd = Math.max(maxProd, prod);
				//System.out.printf("%d elements starting from %d: %d\n", i, j, prod);
			}
		}
		return maxProd;
	}
}
