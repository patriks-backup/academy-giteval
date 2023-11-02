import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class DateiLesen {
    public static void main(String[] args) {
        // Pfad zur Datei, die du lesen möchtest
        String dateiName = "beispiel.txt";

        try {
            // FileReader und BufferedReader erstellen, um die Datei zu lesen
            FileReader fileReader = new FileReader(dateiName);
            BufferedReader bufferedReader = new BufferedReader(fileReader);

            String zeile;

            // Schleife zum Lesen und Ausgeben jeder Zeile
            while ((zeile = bufferedReader.readLine()) != null) {
                System.out.println(zeile);
            }

            // Dateien schließen
            bufferedReader.close();
            fileReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class DateiLesen {
    public static void main(String[] args) {
            // Pfad zur Datei, die du lesen möchtest
	            String dateiName = "beispiel.txt";

		            try {
			                // FileReader und BufferedReader erstellen, um die Datei zu lesen
					            FileReader fileReader = new FileReader(dateiName);
						                BufferedReader bufferedReader = new BufferedReader(fileReader);

								            String zeile;

									                // Schleife zum Lesen und Ausgeben jeder Zeile
											            while ((zeile = bufferedReader.readLine()) != null) {
												                    System.out.println(zeile);
														                }

																            // Dateien schließen
																	                bufferedReader.close();
																			            fileReader.close();
																				            } catch (IOException e) {
																					                e.printStackTrace();
																							        }
																								    }
																								    }
