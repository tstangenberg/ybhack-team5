package ybhack.team5.instascrape;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import kong.unirest.HttpResponse;
import kong.unirest.Unirest;
import lombok.extern.java.Log;
import org.springframework.stereotype.Component;

@Component
@Log
public class ElasticPusher {
    public void pushToElasticSearch(String id, InstagramFame fame) {
        if(fame != null) {
            ObjectMapper objectMapper = new ObjectMapper();
            String json = null;
            try {
                json = objectMapper.writeValueAsString(fame);
                log.info("updating " + id);
                HttpResponse httpResponse = Unirest
                        .post("https://dreng:mobi123@elastic.dreng.ch/insta/_doc/{id}")
                        .routeParam("id", id)
                        .header("Content-Type", "application/json")
                        .body(json)
                        .asEmpty();
                log.info(httpResponse.getStatusText());

            } catch (JsonProcessingException e) {
                e.printStackTrace();
                log.severe(e.getMessage());
            }
        }
    }
}
