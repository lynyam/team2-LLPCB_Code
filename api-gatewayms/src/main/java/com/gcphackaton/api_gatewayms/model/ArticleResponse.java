package com.gcphackaton.api_gatewayms.model;

public class ArticleResponse {
    private String text;          // Texte extrait de l'article
    private String analysis;      // Résultat de l'analyse de la rhétorique
    private String formattedResponse;  // Réponse formatée après analyse

    // Constructeur
    public ArticleResponse() {
    }

    public ArticleResponse(String text, String analysis, String formattedResponse) {
        this.text = text;
        this.analysis = analysis;
        this.formattedResponse = formattedResponse;
    }

    // Getters et Setters
    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getAnalysis() {
        return analysis;
    }

    public void setAnalysis(String analysis) {
        this.analysis = analysis;
    }

    public String getFormattedResponse() {
        return formattedResponse;
    }

    public void setFormattedResponse(String formattedResponse) {
        this.formattedResponse = formattedResponse;
    }
}
