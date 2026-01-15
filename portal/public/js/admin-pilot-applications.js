/**
 * Admin Pilot Applications JavaScript Module
 * Handles API interactions for pilot factory application management
 */

const API_BASE = '/api/auth';
let currentPage = 1;
let currentLimit = 20;
let currentFilters = {};
let allApplications = [];

/**
 * API Client Functions
 */

// Fetch applications with filters and pagination
async function fetchApplications(filters = {}, page = 1, limit = 20) {
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token');
    if (!token) {
        window.location.href = '/auth.html';
        return null;
    }

    try {
        const params = new URLSearchParams({
            page: page,
            limit: limit,
            ...filters
        });

        const response = await fetch(`${API_BASE}/admin/pilot-applications?${params}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/auth.html';
            return null;
        }

        if (!response.ok) {
            throw new Error('Failed to fetch applications');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching applications:', error);
        showToast('Failed to load applications', 'error');
        return null;
    }
}

// Fetch single application detail
async function fetchApplicationDetail(id) {
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token');
    if (!token) {
        window.location.href = '/auth.html';
        return null;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/pilot-applications/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/auth.html';
            return null;
        }

        if (response.status === 404) {
            showToast('Application not found', 'error');
            setTimeout(() => window.location.href = '/admin/pilot-applications.html', 2000);
            return null;
        }

        if (!response.ok) {
            throw new Error('Failed to fetch application details');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching application:', error);
        showToast('Failed to load application details', 'error');
        return null;
    }
}

// Update application status and notes
async function updateApplicationStatus(id, status, notes) {
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token');
    if (!token) {
        window.location.href = '/auth.html';
        return false;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/pilot-applications/${id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: status,
                admin_notes: notes
            })
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/auth.html';
            return false;
        }

        if (!response.ok) {
            throw new Error('Failed to update application');
        }

        const result = await response.json();
        showToast('Application updated successfully', 'success');
        
        // Reload the page to show updated data
        setTimeout(() => window.location.reload(), 1000);
        
        return true;
    } catch (error) {
        console.error('Error updating application:', error);
        showToast('Failed to update application', 'error');
        return false;
    }
}

// Get application statistics
async function getApplicationStats() {
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token');
    if (!token) {
        return null;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/pilot-applications/stats`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch statistics');
        }

        const data = await response.json();
        return data.stats || null;
    } catch (error) {
        console.error('Error fetching stats:', error);
        return null;
    }
}

/**
 * UI Rendering Functions
 */

// Load and display applications
async function loadApplications() {
    const data = await fetchApplications(currentFilters, currentPage, currentLimit);
    
    if (!data) {
        renderEmptyState('Failed to load applications');
        return;
    }

    allApplications = data.applications || [];
    
    if (allApplications.length === 0) {
        renderEmptyState('No applications found');
        return;
    }

    renderApplicationsTable(allApplications);
    renderPagination(data.total || 0, currentPage, currentLimit);
}

// Load and display statistics
async function loadStats() {
    const stats = await getApplicationStats();
    
    if (!stats) {
        return;
    }

    // Update stat cards
    document.getElementById('statTotal').textContent = stats.total || 0;
    document.getElementById('statPending').textContent = stats.pending || 0;
    document.getElementById('statUnderReview').textContent = stats.under_review || 0;
    document.getElementById('statReviewed').textContent = stats.reviewed || 0;
    document.getElementById('statAccepted').textContent = stats.accepted || 0;
}

// Load and display single application detail
async function loadApplicationDetail(id) {
    const data = await fetchApplicationDetail(id);
    
    if (!data || !data.application) {
        return;
    }

    const app = data.application;

    // Hide loading, show content
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('contentArea').style.display = 'block';

    // Update header
    document.getElementById('applicationRef').textContent = app.application_ref || 'N/A';
    document.getElementById('breadcrumbRef').textContent = app.application_ref || 'Details';
    
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = formatStatus(app.status);
    statusBadge.className = 'status-badge status-' + (app.status || 'pending');

    // Company Information
    document.getElementById('companyName').textContent = app.company_name || '-';
    document.getElementById('cityAddress').textContent = app.city_address || '-';
    document.getElementById('companyWebsite').innerHTML = app.company_website 
        ? `<a href="${app.company_website}" target="_blank">${app.company_website}</a>` 
        : '-';

    // Contact Information
    document.getElementById('contactName').textContent = app.contact_name || '-';
    document.getElementById('contactPosition').textContent = app.contact_position || '-';
    document.getElementById('contactEmail').innerHTML = app.contact_email 
        ? `<a href="mailto:${app.contact_email}">${app.contact_email}</a>` 
        : '-';
    document.getElementById('contactPhone').innerHTML = app.contact_phone 
        ? `<a href="tel:${app.contact_phone}">${app.contact_phone}</a>` 
        : '-';

    // Factory Profile
    const sector = app.manufacturing_sector === 'other' && app.manufacturing_sector_other
        ? `Other (${app.manufacturing_sector_other})`
        : (app.manufacturing_sector || '-');
    document.getElementById('manufacturingSector').textContent = sector;
    document.getElementById('numEmployees').textContent = app.num_employees || '-';
    document.getElementById('facilityArea').textContent = app.facility_area || '-';
    document.getElementById('annualElectricity').textContent = app.annual_electricity || '-';
    document.getElementById('numProductionOps').textContent = app.num_production_operations || '-';

    // Digital & Energy Readiness
    document.getElementById('digitalMonitoring').innerHTML = getBooleanBadge(app.digital_monitoring);
    document.getElementById('numDigitalMeters').textContent = app.num_digital_meters || 'N/A';
    document.getElementById('hasScada').innerHTML = getBooleanBadge(app.has_scada);
    document.getElementById('hasEnergyResponsible').textContent = app.has_energy_responsible || '-';
    document.getElementById('digitalMaturity').innerHTML = getMaturityBadge(app.digital_maturity);

    // Participation & Availability
    document.getElementById('willingToParticipate').innerHTML = getBooleanBadge(app.willing_to_participate);
    document.getElementById('confirmsCollaboration').innerHTML = getBooleanBadge(app.confirms_collaboration);
    document.getElementById('preferredMeetingWeek').textContent = app.preferred_meeting_week || 'Not specified';
    document.getElementById('preferredInstallationWeek').textContent = app.preferred_installation_week || 'Not specified';

    // Submission Metadata
    document.getElementById('submittedAt').textContent = formatDate(app.submitted_at);
    document.getElementById('ipAddress').textContent = app.ip_address || '-';
    document.getElementById('userAgent').textContent = app.user_agent || '-';

    // Management Form
    document.getElementById('statusSelect').value = app.status || 'pending';
    document.getElementById('adminNotes').value = app.admin_notes || '';

    // Review Info
    if (app.reviewed_at) {
        document.getElementById('reviewInfo').style.display = 'block';
        document.getElementById('reviewedAt').textContent = formatDate(app.reviewed_at);
        document.getElementById('reviewedBy').textContent = `By: Admin User #${app.reviewed_by || 'Unknown'}`;
    }

    // Timeline
    updateTimeline(app);
}

// Render applications table
function renderApplicationsTable(applications) {
    const tbody = document.getElementById('tableBody');
    
    if (!applications || applications.length === 0) {
        renderEmptyState('No applications found');
        return;
    }

    tbody.innerHTML = applications.map(app => `
        <tr data-app-id="${app.id}">
            <td><a href="/admin/pilot-application-detail.html?id=${app.id}" class="ref-link">${app.application_ref}</a></td>
            <td><strong>${app.company_name}</strong></td>
            <td>${app.contact_name}</td>
            <td><a href="mailto:${app.contact_email}">${app.contact_email}</a></td>
            <td>${app.manufacturing_sector}</td>
            <td>${app.annual_electricity}</td>
            <td>${getMaturityBadge(app.digital_maturity)}</td>
            <td>${getRelativeTime(app.submitted_at)}</td>
            <td>${getStatusBadge(app.status)}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn-small btn-view" onclick="viewApplication(${app.id})">View</button>
                    <button class="btn-small btn-email" onclick="quickEmail('${app.contact_email}', '${app.application_ref}')">Email</button>
                    <button class="btn-small btn-delete" onclick="deleteApplication(${app.id}, '${app.application_ref}', '${app.company_name}')" style="background: #dc3545;">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Render pagination controls
function renderPagination(total, page, limit) {
    if (total === 0) {
        document.getElementById('pagination').style.display = 'none';
        return;
    }

    document.getElementById('pagination').style.display = 'flex';
    
    const totalPages = Math.ceil(total / limit);
    const start = (page - 1) * limit + 1;
    const end = Math.min(page * limit, total);

    // Update info
    document.getElementById('paginationInfo').textContent = 
        `Showing ${start}-${end} of ${total} applications`;

    // Update controls
    const controls = document.getElementById('paginationControls');
    let html = '';

    // Previous button
    if (page > 1) {
        html += `<button class="page-btn" onclick="changePage(${page - 1})">← Prev</button>`;
    }

    // Page numbers (show max 5)
    const startPage = Math.max(1, page - 2);
    const endPage = Math.min(totalPages, page + 2);

    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === page ? 'active' : '';
        html += `<button class="page-btn ${activeClass}" onclick="changePage(${i})">${i}</button>`;
    }

    // Next button
    if (page < totalPages) {
        html += `<button class="page-btn" onclick="changePage(${page + 1})">Next →</button>`;
    }

    controls.innerHTML = html;
}

// Render empty state
function renderEmptyState(message) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = `
        <tr>
            <td colspan="10">
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 8v4M12 16h.01"/>
                    </svg>
                    <h3>No Applications Found</h3>
                    <p>${message || 'Try adjusting your filters'}</p>
                </div>
            </td>
        </tr>
    `;
    document.getElementById('pagination').style.display = 'none';
}

// Update timeline
function updateTimeline(app) {
    const timeline = document.getElementById('timeline');
    document.getElementById('timelineSubmitted').textContent = formatDate(app.submitted_at);

    // Add more timeline items if there are status changes
    if (app.reviewed_at) {
        const reviewItem = document.createElement('div');
        reviewItem.className = 'timeline-item';
        reviewItem.innerHTML = `
            <div class="time">${formatDate(app.reviewed_at)}</div>
            <div class="event">Status changed to "${formatStatus(app.status)}"</div>
        `;
        timeline.appendChild(reviewItem);
    }
}

/**
 * Utility Functions
 */

// Format date
function formatDate(dateString) {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Get relative time
function getRelativeTime(dateString) {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
}

// Format status text
function formatStatus(status) {
    if (!status) return 'Pending';
    
    return status
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Get status badge HTML
function getStatusBadge(status) {
    const text = formatStatus(status);
    return `<span class="status-badge status-${status || 'pending'}">${text}</span>`;
}

// Get maturity badge HTML
function getMaturityBadge(level) {
    if (!level) return '-';
    
    // Normalize maturity level (handle both old and new formats)
    let normalizedLevel = level.toLowerCase();
    if (normalizedLevel.includes('low') || normalizedLevel.includes('manual')) {
        normalizedLevel = 'low';
    } else if (normalizedLevel.includes('medium') || normalizedLevel.includes('some digital')) {
        normalizedLevel = 'medium';
    } else if (normalizedLevel.includes('high') || normalizedLevel.includes('advanced')) {
        normalizedLevel = 'high';
    }
    
    const displayText = normalizedLevel.charAt(0).toUpperCase() + normalizedLevel.slice(1);
    return `<span class="maturity-badge maturity-${normalizedLevel}">${displayText}</span>`;
}

// Get boolean badge HTML
function getBooleanBadge(value) {
    if (value === true || value === 'yes') {
        return '<span class="badge badge-yes">✓ Yes</span>';
    } else if (value === false || value === 'no') {
        return '<span class="badge badge-no">✗ No</span>';
    }
    return '-';
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// Generate CSV from applications
function generateCSV(applications) {
    if (!applications || applications.length === 0) {
        showToast('No data to export', 'error');
        return;
    }

    const headers = [
        'Reference', 'Company', 'Contact Name', 'Email', 'Phone',
        'Sector', 'Employees', 'Facility Area', 'Electricity',
        'Digital Maturity', 'Status', 'Submitted At'
    ];

    const rows = applications.map(app => [
        app.application_ref,
        app.company_name,
        app.contact_name,
        app.contact_email,
        app.contact_phone,
        app.manufacturing_sector,
        app.num_employees,
        app.facility_area,
        app.annual_electricity,
        app.digital_maturity,
        app.status,
        formatDate(app.submitted_at)
    ]);

    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    // Create download
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pilot-applications-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showToast('CSV exported successfully', 'success');
}

// Show toast notification
function showToast(message, type = 'success') {
    // Try to use existing toast if on detail page, otherwise create one
    let toast = document.getElementById('toast');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.className = 'toast ' + type;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

/**
 * Action Handlers
 */

// Refresh data
function refreshData() {
    currentPage = 1;
    loadApplications();
    loadStats();
    showToast('Data refreshed', 'success');
}

// Apply filters
function applyFilters() {
    const status = document.getElementById('filterStatus').value;
    const maturity = document.getElementById('filterMaturity').value;
    const search = document.getElementById('filterSearch').value;
    const sort = document.getElementById('filterSort').value;

    currentFilters = {};
    
    if (status) currentFilters.status = status;
    if (maturity) currentFilters.digital_maturity = maturity;
    if (search) currentFilters.search = search;
    if (sort) currentFilters.sort = sort;

    currentPage = 1;
    loadApplications();
}

// Clear filters
function clearFilters() {
    document.getElementById('filterStatus').value = '';
    document.getElementById('filterMaturity').value = '';
    document.getElementById('filterSearch').value = '';
    document.getElementById('filterSort').value = 'newest';
    
    currentFilters = {};
    currentPage = 1;
    loadApplications();
}

// Change page
function changePage(page) {
    currentPage = page;
    loadApplications();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// View application
function viewApplication(id) {
    window.location.href = `/admin/pilot-application-detail.html?id=${id}`;
}

// Delete application
async function deleteApplication(id, ref, companyName) {
    if (!confirm(`⚠️ Are you sure you want to DELETE this application?\n\nRef: ${ref}\nCompany: ${companyName}\n\nThis action CANNOT be undone!`)) {
        return;
    }
    
    const token = localStorage.getItem('auth_token') || localStorage.getItem('token');
    if (!token) {
        window.location.href = '/auth.html';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/pilot-applications/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast(data.message || 'Application deleted successfully', 'success');
            
            // Remove row from table with animation
            const row = document.querySelector(`tr[data-app-id="${id}"]`);
            if (row) {
                row.style.transition = 'opacity 0.3s ease';
                row.style.opacity = '0';
                setTimeout(() => {
                    row.remove();
                    // Reload to update stats and pagination
                    loadApplications();
                    loadStats();
                }, 300);
            } else {
                // If row not found, just reload
                loadApplications();
                loadStats();
            }
        } else {
            showToast(data.error || 'Failed to delete application', 'error');
        }
    } catch (error) {
        console.error('Error deleting application:', error);
        showToast('Failed to delete application', 'error');
    }
}

// Quick email
function quickEmail(email, ref) {
    const subject = encodeURIComponent(`HumanEnerDIA Pilot Factory - ${ref}`);
    window.location.href = `mailto:${email}?subject=${subject}`;
}

// Export to CSV
function exportToCSV() {
    if (allApplications.length > 0) {
        generateCSV(allApplications);
    } else {
        // Fetch all applications without pagination for export
        fetchApplications(currentFilters, 1, 1000).then(data => {
            if (data && data.applications) {
                generateCSV(data.applications);
            }
        });
    }
}
