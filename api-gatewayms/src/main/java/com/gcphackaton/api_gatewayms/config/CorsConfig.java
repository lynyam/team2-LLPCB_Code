package com.gcphackaton.api_gatewayms.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        String[] extensions = System.getenv("ALLOWED_CHROME_EXTENSION_IDS").split(",");
        // Configure CORS
        for (String extension : extensions) {
            registry.addMapping("/api/**")
                    .allowedOrigins("chrome-extension://" + extension)
                    .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                    .allowedHeaders("*")
                    .allowCredentials(true);
        }
    }
}
