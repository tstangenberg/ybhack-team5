package ybhack.team5.instascrape;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import lombok.Data;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.List;
import java.util.stream.Collectors;

@Data
public class Spieler {

    String name;
    String instagramHandle;

    public static List<Spieler> load() throws IOException, CsvException {

        InputStream resourceAsStream = Spieler.class.getResourceAsStream("/YB-Kader.csv");
        assert resourceAsStream != null;
        CSVReader reader = new CSVReader(new InputStreamReader(resourceAsStream));
        reader.readNext(); // skip header
        List<String[]> myEntries = reader.readAll();

        return myEntries.stream()
                .map(x -> x[0].split(";"))
                .map( x -> {

            Spieler s = new Spieler();
            s.setName(x[1]);
            if (x.length >= 4) {
                s.setInstagramHandle(x[3]);
            } else {
                s.setInstagramHandle(null);
            }

            return s;
        }).collect(Collectors.toList());
    }

}