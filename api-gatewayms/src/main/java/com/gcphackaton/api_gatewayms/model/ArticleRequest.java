package com.gcphackaton.api_gatewayms.model;

public class ArticleRequest {
    private String url;  // URL de l'article à analyser

    // Constructeur
    public ArticleRequest() {
    }

    public ArticleRequest(String url) {
        this.url = url;
    }

    // Getter et Setter
    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
