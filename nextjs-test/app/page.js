// src/app/page.js ou src/pages/index.js

import ArticleProcessor from './ArticleProcessor';

export default function HomePage() {
    return (
        <div>
            <h1>Accueil</h1>
            <ArticleProcessor />
        </div>
    );
}
