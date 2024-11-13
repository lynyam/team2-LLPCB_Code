package com.gcphackaton.api_gatewayms.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // Configure CORS
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:3000")  // Frontend (Next.js)
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // Autoriser les méthodes HTTP
                .allowedHeaders("*")  // Autoriser tous les en-têtes
                .allowCredentials(true); // Autoriser les cookies et autres credentials
    }
}
