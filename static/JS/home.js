//HEADER
const header = document.querySelector('#header');
const headerHeight = header.offsetHeight;

let scrollPositionY = window.scrollY;
let headerHovered = document.querySelector('.page__header:hover') ? true : false;
let scrollTimeOut = 0;

header.addEventListener('mouseenter', () => {
    headerHovered = true;
    scrollPositionY = window.scrollY;
    clearTimeout(scrollTimeOut);
    header.style.display = 'block';
});

header.addEventListener('mouseleave', () => {
    headerHovered = false;
    scrollPositionY = window.scrollY;
    if (scrollPositionY <= headerHeight) {
        header.style.position = 'absolute';
        clearTimeout(scrollTimeOut);
        header.style.display = 'block';
    } else {
        header.style.position = 'fixed';
        if (!headerHovered) {
            scrollTimeOut = setTimeout(() => {
                header.style.display = 'none';
            }, 3000);
        }
    }
});

document.addEventListener('scroll', () => {
    scrollPositionY = window.scrollY;
    clearTimeout(scrollTimeOut);
    header.style.display = 'block';
});

document.addEventListener('scrollend', () => {
    scrollPositionY = window.scrollY;
    if (scrollPositionY <= headerHeight) {
        header.style.position = 'absolute';
        clearTimeout(scrollTimeOut);
        header.style.display = 'block';
    } else {
        header.style.position = 'fixed';
        if (!headerHovered) {
            scrollTimeOut = setTimeout(() => {
                header.style.display = 'none';
            }, 3000);
        }
    }
});



//HOME

//MENU
let menuWidth;
if (document.getElementsByClassName('carousel-item').length * document.getElementsByClassName('carousel-item')[0]){
    menuWidth = document.getElementsByClassName('carousel-item').length * document.getElementsByClassName('carousel-item')[0].clientWidth;
}
//SETTING THE NEW SLIDE
let menuScrollPosition = 0;
let reviewScrollPosition = 0;
let int;

const mouseUp = function () {
    clearInterval(int);
};

const nextMouseDown = (e) => {
    int = setInterval(() => {
        if (e.target.getAttribute('id') == "next-menu") {
            if (menuScrollPosition < menuWidth) {
                menuScrollPosition += 100;
                $(e.target.parentNode.previousElementSibling.previousElementSibling).animate({ scrollLeft: menuScrollPosition }, 600);
            }
        } else {
            if (reviewScrollPosition < menuWidth) {
                reviewScrollPosition += 100;
                $(e.target.parentNode.previousElementSibling.previousElementSibling).animate({ scrollLeft: reviewScrollPosition }, 600);
            }
        }
    }, 400);
};

const prevMouseDown = (e) => {
    int = setInterval(() => {
        if (e.target.getAttribute('id') == "prev-menu") {
            if (menuScrollPosition > 0) {
                menuScrollPosition -= 100;
                $(e.target.parentNode.previousElementSibling).animate({ scrollLeft: menuScrollPosition }, 600);
            }
        }
        else {
            if (reviewScrollPosition > 0) {
                reviewScrollPosition -= 100;
                $(e.target.parentNode.previousElementSibling).animate({ scrollLeft: reviewScrollPosition }, 600);
            }
        }
    }, 400);
};

$(".carousel-control-next").mousedown(nextMouseDown).mouseup(mouseUp);


$(".carousel-control-prev").mousedown(prevMouseDown).mouseup(mouseUp);

//RADIO BUTTONS
const menuRadios = document.getElementsByClassName('radio-btn');
for (const radio of menuRadios) {
    radio.addEventListener('click', () => {
        const chefItems = document.getElementsByClassName('chef-item');
        const mealItems = document.getElementsByClassName('meal-item');
        scrollPosition = 0;
        $('.carousel-inner').animate({ scrollLeft: scrollPosition }, 600);
        if (radio.children[0].value === "meals") {
            for (const chef of chefItems) {
                chef.style.display = "none";
            }
            for (const meal of mealItems) {
                meal.style.display = "block";
            }
            menuWidth = mealItems.length * mealItems[0].clientWidth / 3;
        } else {
            for (const meal of mealItems) {
                meal.style.display = "none";
            }
            for (const chef of chefItems) {
                chef.style.display = "block";
            }
            menuWidth = chefItems.length * chefItems[0].clientWidth / 3;
        }
    })
}

//SEARCH
if (document.querySelector('.search-form')) {
    document.querySelector('.search-form').addEventListener('submit', (event) => {
        event.preventDefault();


        const query = document.querySelector('.search-for').value.toLowerCase();
        const allCards = document.querySelectorAll('.menu-item');

        let cardsCount = 0;

        for (const radio of menuRadios) {
            radio.children[0].checked = false;
        }

        for (const card of allCards) {
            if (card.getElementsByClassName('card-title')[0].innerHTML.toLowerCase().includes(query)) {
                card.style.display = "block";
                cardsCount++;
            } else {
                card.style.display = "none";
            }
        }
        menuWidth = cardsCount * allCards[0].clientWidth / 3;
    });
}


//Profile
//Side bar
const btn = document.querySelector(".profile-toggle-btn");
const sidebar = document.querySelector(".profile-sidebar");
const main = document.querySelector(".profile-main");
const profileHeader = document.querySelector(".header");
const profileFooter = document.querySelector(".footer");

if (btn) {
    btn.addEventListener('click', () => {
        sidebar.classList.toggle("expand");
        main.classList.toggle("expand");
        profileHeader.classList.toggle("expand");
        profileFooter.classList.toggle("expand");
    })
}

//adding ingredients to list
if (document.getElementById("addMeal-ingredient-btn")) {
    document.getElementById("addMeal-ingredient-btn").onclick = function () {
        let ingridient = document.getElementById("addMeal-ingredient-txt").value;
        if (ingridient) {
            document.getElementById("addMeal-ingredients").innerHTML += "<li>" + ingridient + "<li><hr>";
            document.getElementById("addMealIngridientList").value += ingridient + ",";
            document.getElementById("addMeal-ingredient-txt").value = "";
        }
    }
}

//home Post
for (element of document.getElementsByName("homeSubmitChef")){
    element.addEventListener('click', function (event) {
        for (element of document.getElementsByName("homeSubmittedChef")){
            element.value = event.target.id;
        } 
        return true;
    });
}

for (element of document.getElementsByName("homeSubmitMeal")){
    element.addEventListener('click', function (event) {
        for (element of document.getElementsByName("homeSubmittedMeal")){
            element.value = event.target.id;
        } 
        return true;
    });
}
