package ybhack.team5.instascrape;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import kong.unirest.HttpRequestWithBody;
import kong.unirest.HttpResponse;
import kong.unirest.Unirest;
import lombok.extern.java.Log;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Log
public class ElasticPusher {

    @Value("${ELASTIC_USER}")
    private String elasticUser;

    @Value("${ELASTIC_PASS}")
    private String elasticPass;

    @Value("${ELASTIC_URL}")
    private String elasticUrl;

    public void pushToElasticSearch(String id, InstagramFame fame) {
        if(fame != null) {
            ObjectMapper objectMapper = new ObjectMapper();
            String json = null;
            try {
                json = objectMapper.writeValueAsString(fame);
                log.info("updating " + id);
                HttpRequestWithBody post = Unirest
                        .post(elasticUrl);
                if (!elasticUser.isEmpty()) {
                    post = post.routeParam("user", elasticUser);
                }
                if (!elasticPass.isEmpty()) {
                    post = post.routeParam("pass", elasticPass);
                }

                HttpResponse httpResponse = post
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
