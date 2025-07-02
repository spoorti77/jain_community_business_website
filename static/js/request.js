// Global variables
let familyMembers = []
let events = []
let filteredMembers = []
let filteredEvents = []
let selectedMembers = []
let selectedEvents = []
let currentMemberView = "cards"
let currentEventView = "cards"
let currentMemberSort = "name"
let currentEventSort = "date"
let viewingMemberId = null
let viewingEventId = null

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
  loadData()
  updateDashboard()
  renderFamilyMembers()
  renderEvents()
})


// Tab switching
function switchTab(tabName) {
  // Remove active class from all nav items and tab contents
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active")
  })
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active")
  })

  // Add active class to clicked nav item and corresponding tab content
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("active")
  document.getElementById(`${tabName}-tab`).classList.add("active")

  // Close sidebar on mobile after tab switch
  if (window.innerWidth <= 768) {
    document.getElementById("sidebar").classList.remove("active")
  }
}

// Toggle sidebar for mobile
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active")
}

// Modal functions
function openModal(modalId) {
  document.getElementById(modalId).classList.add("active")
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove("active")
  // Reset forms
  const form = document.querySelector(`#${modalId} form`)
  if (form) {
    form.reset()
  }
}

// View toggle functions
function toggleView(viewType, section = "members") {
  if (section === "members") {
    currentMemberView = viewType

    // Update view buttons
    document.querySelectorAll("#family-tab .view-btn").forEach((btn) => {
      btn.classList.remove("active")
    })
    document.querySelector(`#family-tab [data-view="${viewType}"]`).classList.add("active")

    // Show/hide views
    document.getElementById("members-cards-view").style.display = viewType === "cards" ? "grid" : "none"
    document.getElementById("members-table-view").style.display = viewType === "table" ? "block" : "none"

    renderFamilyMembers()
  } else if (section === "events") {
    currentEventView = viewType

    // Update view buttons
    document.querySelectorAll("#events-tab .view-btn").forEach((btn) => {
      btn.classList.remove("active")
    })
    document.querySelector(`#events-tab [data-view="${viewType}"]`).classList.add("active")

    // Show/hide views
    document.getElementById("events-cards-view").style.display = viewType === "cards" ? "grid" : "none"
    document.getElementById("events-table-view").style.display = viewType === "table" ? "block" : "none"

    renderEvents()
  }
}

// Bulk selection functions
function toggleSelectAll(type) {
  const checkboxes = document.querySelectorAll(`input[name="${type}-select"]`)
  const selectAllCheckbox = document.getElementById(`select-all-${type}`)
  const tableSelectAllCheckbox = document.getElementById(`table-select-all-${type}`)

  const isChecked = selectAllCheckbox ? selectAllCheckbox.checked : tableSelectAllCheckbox.checked

  checkboxes.forEach((checkbox) => {
    checkbox.checked = isChecked
  })

  // Sync both select all checkboxes
  if (selectAllCheckbox) selectAllCheckbox.checked = isChecked
  if (tableSelectAllCheckbox) tableSelectAllCheckbox.checked = isChecked

  updateBulkActions(type)
}

function updateBulkActions(type) {
  const checkboxes = document.querySelectorAll(`input[name="${type}-select"]:checked`)
  const count = checkboxes.length
  const countElement = document.getElementById(`selected-${type}-count`)
  const bulkActions = document.getElementById(`${type.slice(0, -1)}-bulk-actions`)

  countElement.textContent = `(${count} selecte  -1)}-bulk-actions\`);
    
    countElement.textContent = \`(${count} selected)`

  if (count > 0) {
    bulkActions.classList.add("active")
  } else {
    bulkActions.classList.remove("active")
  }

  // Update selected arrays
  if (type === "members") {
    selectedMembers = Array.from(checkboxes).map((cb) => cb.value)
  } else if (type === "events") {
    selectedEvents = Array.from(checkboxes).map((cb) => cb.value)
  }
}

// Bulk delete functions
function bulkDeleteMembers() {
  if (selectedMembers.length === 0) return

  if (confirm(`Are you sure you want to delete ${selectedMembers.length} family member(s)?`)) {
    familyMembers = familyMembers.filter((member) => !selectedMembers.includes(member.id))
    selectedMembers = []
    saveData()
    updateDashboard()
    renderFamilyMembers()
    updateBulkActions("members")
  }
}

function bulkDeleteEvents() {
  if (selectedEvents.length === 0) return

  if (confirm(`Are you sure you want to delete ${selectedEvents.length} event(s)?`)) {
    events = events.filter((event) => !selectedEvents.includes(event.id))
    selectedEvents = []
    saveData()
    updateDashboard()
    renderEvents()
    updateBulkActions("events")
  }
}

// Export functions
function exportMembers() {
  const dataToExport =
    selectedMembers.length > 0 ? familyMembers.filter((member) => selectedMembers.includes(member.id)) : familyMembers

  const dataStr = JSON.stringify(dataToExport, null, 2)
  const dataBlob = new Blob([dataStr], { type: "application/json" })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement("a")
  link.href = url
  link.download = "family-members.json"
  link.click()
  URL.revokeObjectURL(url)
}

function exportEvents() {
  const dataToExport = selectedEvents.length > 0 ? events.filter((event) => selectedEvents.includes(event.id)) : events

  const dataStr = JSON.stringify(dataToExport, null, 2)
  const dataBlob = new Blob([dataStr], { type: "application/json" })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement("a")
  link.href = url
  link.download = "family-events.json"
  link.click()
  URL.revokeObjectURL(url)
}

// Filter and sort functions
function filterMembers() {
  const searchTerm = document.getElementById("member-search").value.toLowerCase()
  const relationshipFilter = document.getElementById("relationship-filter").value

  filteredMembers = familyMembers.filter((member) => {
    const matchesSearch =
      member.name.toLowerCase().includes(searchTerm) ||
      member.email.toLowerCase().includes(searchTerm) ||
      member.phone.includes(searchTerm)

    const matchesRelationship = !relationshipFilter || member.relationship === relationshipFilter

    return matchesSearch && matchesRelationship
  })

  sortMembers(currentMemberSort, false)
  renderFamilyMembers()
}

function filterEvents() {
  const searchTerm = document.getElementById("event-search").value.toLowerCase()
  const statusFilter = document.getElementById("event-status-filter").value
  const monthFilter = document.getElementById("event-month-filter").value

  filteredEvents = events.filter((event) => {
    const matchesSearch =
      event.title.toLowerCase().includes(searchTerm) ||
      event.location.toLowerCase().includes(searchTerm) ||
      event.description.toLowerCase().includes(searchTerm)

    const eventDate = new Date(event.date)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    let matchesStatus = true
    if (statusFilter === "upcoming") {
      matchesStatus = eventDate > today
    } else if (statusFilter === "today") {
      matchesStatus = eventDate.toDateString() === today.toDateString()
    } else if (statusFilter === "past") {
      matchesStatus = eventDate < today
    }

    const matchesMonth = !monthFilter || eventDate.getMonth() === Number.parseInt(monthFilter)

    return matchesSearch && matchesStatus && matchesMonth
  })

  sortEvents(currentEventSort, false)
  renderEvents()
}

function sortMembers(sortBy, updateButton = true) {
  currentMemberSort = sortBy

  if (updateButton) {
    document.querySelectorAll("#family-tab .sort-btn").forEach((btn) => {
      btn.classList.remove("active")
    })
    document.querySelector(`#family-tab [data-sort="${sortBy}"]`).classList.add("active")
  }

  filteredMembers.sort((a, b) => {
    if (sortBy === "name") {
      return a.name.localeCompare(b.name)
    } else if (sortBy === "age") {
      const ageA = a.birthday ? calculateAge(a.birthday) : 0
      const ageB = b.birthday ? calculateAge(b.birthday) : 0
      return ageB - ageA // Descending order
    }
    return 0
  })

  renderFamilyMembers()
}

function sortEvents(sortBy, updateButton = true) {
  currentEventSort = sortBy

  if (updateButton) {
    document.querySelectorAll("#events-tab .sort-btn").forEach((btn) => {
      btn.classList.remove("active")
    })
    document.querySelector(`#events-tab [data-sort="${sortBy}"]`).classList.add("active")
  }

  filteredEvents.sort((a, b) => {
    if (sortBy === "date") {
      return new Date(a.date) - new Date(b.date)
    } else if (sortBy === "title") {
      return a.title.localeCompare(b.title)
    }
    return 0
  })

  renderEvents()
}

// Utility functions
function calculateAge(birthday) {
  const today = new Date()
  const birthDate = new Date(birthday)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }

  return age
}

function getEventStatus(eventDate) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const event = new Date(eventDate)
  event.setHours(0, 0, 0, 0)

  if (event.getTime() === today.getTime()) {
    return "today"
  } else if (event > today) {
    return "upcoming"
  } else {
    return "past"
  }
}

function getStatusClass(status) {
  switch (status) {
    case "today":
      return "status-today"
    case "upcoming":
      return "status-upcoming"
    case "past":
      return "status-past"
    default:
      return "status-upcoming"
  }
}

function getStatusText(status) {
  switch (status) {
    case "today":
      return "Today"
    case "upcoming":
      return "Upcoming"
    case "past":
      return "Past"
    default:
      return "Upcoming"
  }
}

// Family Member functions
function openAddMemberModal() {
  openModal("add-member-modal")
}


function closeModal(modalId) {
  document.getElementById(modalId).classList.remove("active")
  // Reset forms
  const form = document.querySelector(`#${modalId} form`)
  if (form) {
    form.reset()
  }
}


function editMemberFromView() {
  closeModal("view-member-modal")
  openEditMemberModal(viewingMemberId)
}

function deleteFamilyMember(memberId) {
  if (confirm("Are you sure you want to delete this family member?")) {
    familyMembers = familyMembers.filter((member) => member.id !== memberId)
    saveData()
    updateDashboard()
    renderFamilyMembers()
    renderEvents() // Re-render events to update attendee lists
  }
}





// Update dashboard statistics and content
function updateDashboard() {
  // Update statistics
  document.getElementById("total-members").textContent = familyMembers.length
  document.getElementById("total-events").textContent = events.length

  const upcomingEvents = getUpcomingEvents()
  const upcomingBirthdays = getUpcomingBirthdays()

  document.getElementById("upcoming-events-count").textContent = upcomingEvents.length
  document.getElementById("upcoming-birthdays-count").textContent = upcomingBirthdays.length
}



// Get upcoming birthdays
function getUpcomingBirthdays() {
  const today = new Date()
  const currentMonth = today.getMonth()
  const currentDay = today.getDate()

  return familyMembers.filter((member) => {
    if (!member.birthday) return false
    const birthday = new Date(member.birthday)
    const memberMonth = birthday.getMonth()
    const memberDay = birthday.getDate()

    // Check if birthday is within next 30 days
    if (memberMonth === currentMonth) {
      return memberDay >= currentDay
    } else if (memberMonth === (currentMonth + 1) % 12) {
      return memberDay <= currentDay
    }
    return false
  })
}





// Close modal when clicking outside
document.querySelectorAll(".modal-overlay").forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("active")
    }
  })
})

// Close sidebar when clicking outside on mobile
document.addEventListener("click", (e) => {
  const sidebar = document.getElementById("sidebar")
  const toggle = document.querySelector(".mobile-menu-toggle")

  if (
    window.innerWidth <= 768 &&
    sidebar.classList.contains("active") &&
    !sidebar.contains(e.target) &&
    !toggle.contains(e.target)
  ) {
    sidebar.classList.remove("active")
  }
})

// Handle window resize
window.addEventListener("resize", () => {
  if (window.innerWidth > 768) {
    document.getElementById("sidebar").classList.remove("active")
  }
})
