package ybhack.team5.instascrape;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class InstagramHandleScraperTest {

    private String html = "\"interactionType\":\"http:\\/\\/schema.org\\/FollowAction\",\"userInteractionCount\":\"10467\"}},\"image\":\"https";

    @Test
    void testInteractionCountExtract() {
        InstagramHandleScraper scraper = new InstagramHandleScraper();
        Integer count = scraper.extractInteractionCount(html);
        assertEquals(count, 10467);
    }
}