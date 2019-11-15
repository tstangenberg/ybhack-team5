package ybhack.team5.instascrape;

import com.opencsv.exceptions.CsvException;
import lombok.extern.java.Log;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;
import java.util.List;

@Log
@SpringBootApplication
public class InstaScrapeApplication implements CommandLineRunner {

    @Autowired
    InstagramHandleScraper instagramHandleScraper;

    @Autowired
    ElasticPusher elasticPusher;

    private static Logger LOG = LoggerFactory
            .getLogger(InstaScrapeApplication.class);

    public static void main(String[] args) {
        LOG.info("STARTING THE APPLICATION");
        SpringApplication.run(InstaScrapeApplication.class, args);
        LOG.info("APPLICATION FINISHED");
    }

    @Override
    public void run(String... args) throws IOException, CsvException {
        LOG.info("EXECUTING : command line runner");
        List<Spieler> alle = Spieler.load();
        for (Spieler spieler : alle) {
            log.info("Instagram fuer " + spieler.name);
            String handle = spieler.instagramHandle;
            String name = spieler.name;
            if (handle != null) {
                InstagramFame fame = instagramHandleScraper.scrape(handle, name);
                if (fame != null) {
                    elasticPusher.pushToElasticSearch(handle, fame);
                }
            }
        }
    }

}