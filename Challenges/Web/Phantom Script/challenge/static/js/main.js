document.addEventListener("DOMContentLoaded", function () {
  const articles = [
    {
      name: "The Witch's Curse",
      description:
        "Explore the eerie tale of the infamous witch of Raven Hollow, whose curse turned an entire village into shadows. Unravel the dark history and learn about the brave souls who sought to lift the curse.",
      author: "Xclow3n",
      image: "/static/images/one.webp",
    },
    {
      name: "Haunted Woods of Dreadfall",
      description:
        "Journey into the haunted forest where lost souls wander and strange creatures lurk. Discover the chilling stories behind those who entered Dreadfall and never returned.",
      author: "Xclow3n",
      image: "/static/images/second.webp",
    },
    {
      name: "The Phantom's Lament",
      description:
        "Listen to the tragic tale of the Phantom of Blackmoor Manor, who roams the halls in search of a long-lost love. This article delves deep into the ghostly appearances and the spine-tingling encounters within the manor.",
      author: "Xclow3n",
      image: "/static/images/third.webp",
    },
    {
      name: "The Blood Moon Awakening",
      description:
        "On a night when the blood moon rises, the ancient vampires of the Nightshade clan awaken from their centuries-long slumber. Emerging from their crypts, these fearsome beings once terrorized the realm with their insatiable thirst for blood. Cloaked in the shadows of the graveyard, their red eyes pierce the darkness, and their fangs gleam under the crimson light of the moon. Legends say that on nights like these, the Nightshade vampires gather to plan their return, their influence growing as the moon turns red. This article delves into the origins of the blood moon awakening and the vampire hunters sworn to stop them.",
      author: "Xclow3n",
      image: "/static/images/fourth.webp",
    },
    {
      name: "The Pumpkin King's Return",
      description:
        "Every century, the Pumpkin King rises from his cursed slumber to wreak havoc during the harvest festival. This article traces the origins of the Pumpkin King and the forgotten rituals used to seal him away.",
      author: "Xclow3n",
      image: "/static/images/fifth.webp",
    },
  ];

  const articlesContainer = document.querySelector(".articles-container");
  const searchInput = document.querySelector(
    'input[placeholder="Search the Shadows..."]',
  );
  const searchButton = document.getElementById("searchBTN");
  const searchResultsHeading = document.createElement("h2");

  searchInput.parentNode.parentNode.appendChild(searchResultsHeading);

  // Function to render the filtered articles
  function renderArticles(filteredArticles) {
    articlesContainer.innerHTML = ""; // Clear the current articles
    filteredArticles.forEach((article) => {
      const articleElement = document.createElement("div");
      articleElement.classList.add("rpgui-container", "framed-golden-2");
      articleElement.style.marginBottom = "20px";

      articleElement.innerHTML = `
        <div class="content">
            <img src="${article.image}" />
            <div style="margin-left: 10px; color: #f8e9c4;">
                <h4 style="color: white; font-size: 24px;">${article.name}</h4>
                <p style="font-size: 14px; margin: 10px 0;">${article.description}</p>
                <p style="font-size: 14px; font-style: italic;">Author: ${article.author}</p>
                <button style="height: 30px;" class="rpgui-button">View</button>
            </div>
        </div>
      `;

      articlesContainer.appendChild(articleElement);
    });
  }

  // Function to filter the articles based on the query
  function filterArticles(query) {
    const lowerCaseQuery = query.toLowerCase();
    return articles.filter(
      (article) =>
        article.name.toLowerCase().includes(lowerCaseQuery) ||
        article.description.toLowerCase().includes(lowerCaseQuery) ||
        article.author.toLowerCase().includes(lowerCaseQuery),
    );
  }

  // Function to trigger the search and render the results
  function applySearch(query) {
    const filteredArticles = filterArticles(query);

    // Update search results heading
    if (query.trim() !== "") {
      searchResultsHeading.innerHTML = `Results for: "${query}"`;
      searchResultsHeading.style.display = "block";
    } else {
      searchResultsHeading.style.display = "none";
    }

    renderArticles(filteredArticles); // Render filtered articles
  }

  // Function to handle the click on the search button
  searchButton.addEventListener("click", function () {
    const query = searchInput.value;
    
    // First render the articles
    applySearch(query);
    
    // Then send the fetch request to trigger the bot
    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Bot triggered:", data.message);
      })
      .catch((error) => {
        console.error("Error triggering bot:", error);
      });
  });

  // Check if there's a `q` query parameter in the URL and trigger search if it exists
  const urlParams = new URLSearchParams(window.location.search);
  const queryParam = urlParams.get("q");

  if (queryParam) {
    // Set the search input value to the query parameter
    searchInput.value = queryParam;

    // Trigger search based on the query parameter without sending a fetch request
    applySearch(queryParam);
  }

  // Initial load: render all articles
  renderArticles(articles);
});
