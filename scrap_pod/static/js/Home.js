function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    document.addEventListener("click", closeNavOnClickOutside);
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.removeEventListener("click", closeNavOnClickOutside);
  }

  function closeNavOnClickOutside(event) {
    if (
      !event.target.closest(".sidenav") &&
      !event.target.closest(".hamburger")
    ) {
      closeNav();
    }
  }

  function toggleDropdown(id) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var currentDropdown = document.getElementById(id);

    // Hide all dropdowns except the current one
    for (var i = 0; i < dropdowns.length; i++) {
      if (dropdowns[i] !== currentDropdown) {
        dropdowns[i].style.display = "none";
      }
    }

    // Toggle the current dropdown
    if (currentDropdown.style.display === "block") {
      currentDropdown.style.display = "none";
    } else {
      currentDropdown.style.display = "block";
    }
  }
  var currentlyOpenMenu = null;

  function toggleSubMenu(menuItemIndex) {
    // event.preventDefault(); // Prevent default action

    var submenuContainer = document.getElementById("sub-product");

    if (currentlyOpenMenu === menuItemIndex) {
      submenuContainer.style.display = "none";
      currentlyOpenMenu = null;
      return;
    }

    currentlyOpenMenu = menuItemIndex;

    var menuItems = document.getElementsByClassName("menu-item");
    var clickedMenuItem = menuItems[menuItemIndex - 1];
    var rect = clickedMenuItem.getBoundingClientRect();

    submenuContainer.style.top = rect.top + "px";
    submenuContainer.style.left = rect.right + "px";
    submenuContainer.style.display = "block";

    document.addEventListener("click", handleOutsideClick);
  }

  function handleOutsideClick(event) {
    var submenuContainer = document.getElementById("sub-product");

    if (
      !submenuContainer.contains(event.target) &&
      !Array.from(document.getElementsByClassName("menu-item")).some((item) =>
        item.contains(event.target)
      )
    ) {
      submenuContainer.style.display = "none";
      currentlyOpenMenu = null;
      document.removeEventListener("click", handleOutsideClick);
    }
  }
