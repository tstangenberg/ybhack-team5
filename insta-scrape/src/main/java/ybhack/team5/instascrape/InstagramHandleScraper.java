package ybhack.team5.instascrape;

import kong.unirest.HttpResponse;
import kong.unirest.Unirest;
import lombok.extern.java.Log;
import org.springframework.stereotype.Service;

import java.util.logging.Level;

@Log
@Service
public class InstagramHandleScraper {

    public InstagramFame scrape(String handle, String name) {

        HttpResponse<String> httpResponse = Unirest.get("https://www.instagram.com/{handle}")
                .routeParam("handle", handle)
                .asString();
        if (httpResponse.isSuccess()) {
            String responseBody = httpResponse.getBody();
            InstagramFame fame = new InstagramFame(name);
            fame.setFollower(extractInteractionCount(responseBody));
            fame.setPosts(extractPostCount(responseBody));
            log.info(fame.toString());
            return fame;
        }
        return null;

    }

    public Integer extractInteractionCount(String text) {
        try {
            String userInteractionCount = "userInteractionCount";
            int userInteractionCountStart = text.indexOf(userInteractionCount);
            int start = userInteractionCountStart + userInteractionCount.length() + 3;
            int end = text.indexOf("\"", start);
            String substring = text.substring(start, end);
            return Integer.parseInt(substring);
        } catch (Exception e) {
            log.log(Level.SEVERE, e.getMessage());
            return 0;
        }
    }

    public Integer extractPostCount(String text) {
        try {
            String postCount = "edge_owner_to_timeline_media\":{\"count\":";
            int userInteractionCountStart = text.indexOf(postCount);
            int start = userInteractionCountStart + postCount.length();
            int end = text.indexOf(",", start);
            String substring = text.substring(start, end);
            return Integer.parseInt(substring);
        } catch (Exception e) {
            log.log(Level.SEVERE, e.getMessage());
            return 0;
        }
    }

}
