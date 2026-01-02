// Pilot Factory Application Form - Client-side Logic
// Handles validation, conditional fields, and submission

(function() {
    'use strict';

    // DOM Elements
    const form = document.getElementById('pilot-factory-form');
    const submitButton = document.getElementById('submitButton');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const messageBox = document.getElementById('messageBox');

    // Conditional field elements
    const sectorRadios = document.querySelectorAll('input[name="manufacturing_sector"]');
    const sectorOtherField = document.getElementById('sector_other_field');
    const sectorOtherInput = document.getElementById('manufacturing_sector_other');

    const monitoringRadios = document.querySelectorAll('input[name="digital_monitoring"]');
    const monitoringDetails = document.getElementById('monitoring_details');
    const numDigitalMetersSelect = document.getElementById('num_digital_meters');
    const scadaRadios = document.querySelectorAll('input[name="has_scada"]');

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', function() {
        initializeConditionalFields();
        initializeValidation();
        initializeFormSubmission();
        makeRadioOptionsClickable();
    });

    // ==================== CONDITIONAL FIELDS ====================

    function initializeConditionalFields() {
        // Manufacturing Sector - Show "Other" input
        sectorRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'Other') {
                    sectorOtherField.classList.add('show');
                    sectorOtherInput.setAttribute('required', 'required');
                } else {
                    sectorOtherField.classList.remove('show');
                    sectorOtherInput.removeAttribute('required');
                    sectorOtherInput.value = '';
                }
            });
        });

        // Digital Monitoring - Show meters and SCADA questions
        monitoringRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'yes') {
                    monitoringDetails.classList.add('show');
                    numDigitalMetersSelect.setAttribute('required', 'required');
                    // Set SCADA radios as required
                    scadaRadios.forEach(r => r.setAttribute('required', 'required'));
                } else {
                    monitoringDetails.classList.remove('show');
                    numDigitalMetersSelect.removeAttribute('required');
                    numDigitalMetersSelect.value = '';
                    // Remove SCADA requirement and clear selection
                    scadaRadios.forEach(r => {
                        r.removeAttribute('required');
                        r.checked = false;
                    });
                }
            });
        });
    }

    // ==================== REAL-TIME VALIDATION ====================

    function initializeValidation() {
        // Email validation
        const emailInput = document.getElementById('contact_email');
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });

        // Phone validation
        const phoneInput = document.getElementById('contact_phone');
        phoneInput.addEventListener('blur', function() {
            validatePhone(this);
        });

        // Required text fields
        const requiredTextFields = form.querySelectorAll('input[type="text"][required], input[type="email"][required], input[type="tel"][required], textarea[required]');
        requiredTextFields.forEach(field => {
            field.addEventListener('blur', function() {
                validateRequired(this);
            });
        });

        // URL validation (optional but validate if filled)
        const urlInput = document.getElementById('company_website');
        if (urlInput) {
            urlInput.addEventListener('blur', function() {
                if (this.value.trim()) {
                    validateURL(this);
                }
            });
        }
    }

    function validateEmail(input) {
        const email = input.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const errorDiv = document.getElementById('error_' + input.id);

        if (!email) {
            showError(input, errorDiv, 'Email is required');
            return false;
        }

        if (!emailRegex.test(email)) {
            showError(input, errorDiv, 'Please enter a valid email address');
            return false;
        }

        showSuccess(input, errorDiv);
        return true;
    }

    function validatePhone(input) {
        const phone = input.value.trim();
        const errorDiv = document.getElementById('error_' + input.id);

        if (!phone) {
            showError(input, errorDiv, 'Phone number is required');
            return false;
        }

        if (phone.length < 7) {
            showError(input, errorDiv, 'Phone number must be at least 7 characters');
            return false;
        }

        showSuccess(input, errorDiv);
        return true;
    }

    function validateRequired(input) {
        const value = input.value.trim();
        const errorDiv = document.getElementById('error_' + input.id);

        if (!value) {
            showError(input, errorDiv, input.placeholder || 'This field is required');
            return false;
        }

        showSuccess(input, errorDiv);
        return true;
    }

    function validateURL(input) {
        const url = input.value.trim();
        const urlRegex = /^https?:\/\/.+/;
        
        if (url && !urlRegex.test(url)) {
            input.classList.add('field-invalid');
            input.classList.remove('field-valid');
            return false;
        }

        input.classList.add('field-valid');
        input.classList.remove('field-invalid');
        return true;
    }

    function showError(input, errorDiv, message) {
        input.classList.add('field-invalid');
        input.classList.remove('field-valid');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }
    }

    function showSuccess(input, errorDiv) {
        input.classList.add('field-valid');
        input.classList.remove('field-invalid');
        if (errorDiv) {
            errorDiv.classList.remove('show');
        }
    }

    // ==================== FORM SUBMISSION ====================

    function initializeFormSubmission() {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous errors
            clearErrorStyling();
            
            // Validate form before submission
            if (!validateForm()) {
                return; // Error UI already shown by validateForm()
            }

            // Check honeypot (anti-spam)
            const honeypot = form.querySelector('input[name="company_url_check"]');
            if (honeypot && honeypot.value !== '') {
                console.warn('Honeypot triggered - potential spam');
                showMessage('There was an error processing your submission. Please try again.', 'error');
                return;
            }

            // Collect and submit data
            submitApplication();
        });
    }

    function validateForm() {
        let isValid = true;
        let errors = [];
        hideMessage();
        
        // Clear previous error styling
        clearErrorStyling();

        // Validate required text fields
        const requiredFields = [
            { id: 'company_name', label: 'Company Name' },
            { id: 'city_address', label: 'City & Address' },
            { id: 'contact_name', label: 'Contact Person Name' },
            { id: 'contact_position', label: 'Contact Position' },
            { id: 'contact_email', label: 'Email Address' },
            { id: 'contact_phone', label: 'Phone Number' }
        ];

        requiredFields.forEach(fieldInfo => {
            const field = document.getElementById(fieldInfo.id);
            if (!field.value.trim()) {
                const errorDiv = document.getElementById('error_' + fieldInfo.id);
                showError(field, errorDiv, fieldInfo.label + ': This field is required');
                errors.push({ id: fieldInfo.id, label: fieldInfo.label, message: 'This field is required' });
                isValid = false;
            }
        });

        // Validate email
        const emailField = document.getElementById('contact_email');
        if (emailField.value.trim() && !validateEmail(emailField)) {
            errors.push({ id: 'contact_email', label: 'Email Address', message: 'Invalid email format' });
            isValid = false;
        }

        // Validate phone
        const phoneField = document.getElementById('contact_phone');
        if (phoneField.value.trim() && !validatePhone(phoneField)) {
            errors.push({ id: 'contact_phone', label: 'Phone Number', message: 'Invalid phone number' });
            isValid = false;
        }

        // Validate radio groups
        const radioGroups = [
            { name: 'manufacturing_sector', label: 'Manufacturing Sector' },
            { name: 'num_employees', label: 'Number of Employees' },
            { name: 'facility_area', label: 'Facility Area' },
            { name: 'annual_electricity', label: 'Annual Electricity Consumption' },
            { name: 'num_production_operations', label: 'Production Operations' },
            { name: 'digital_monitoring', label: 'Digital Monitoring' },
            { name: 'has_energy_responsible', label: 'Energy Responsible Person' },
            { name: 'digital_maturity', label: 'Digital Maturity Level' },
            { name: 'willing_to_participate', label: 'Willing to Participate' }
        ];

        radioGroups.forEach(groupInfo => {
            const checked = form.querySelector(`input[name="${groupInfo.name}"]:checked`);
            if (!checked) {
                const errorDiv = document.getElementById('error_' + groupInfo.name);
                if (errorDiv) {
                    errorDiv.textContent = groupInfo.label + ': Please select an option';
                    errorDiv.classList.add('show');
                }
                errors.push({ id: 'error_' + groupInfo.name, label: groupInfo.label, message: 'Please select an option' });
                isValid = false;
            }
        });

        // Validate conditional "Other" sector
        const sectorOther = document.getElementById('sector_other');
        if (sectorOther && sectorOther.checked) {
            const otherInput = document.getElementById('manufacturing_sector_other');
            if (!otherInput.value.trim()) {
                const errorDiv = document.getElementById('error_manufacturing_sector_other');
                showError(otherInput, errorDiv, 'Manufacturing Sector (Other): Please specify your sector');
                errors.push({ id: 'manufacturing_sector_other', label: 'Manufacturing Sector (Other)', message: 'Please specify' });
                isValid = false;
            }
        }

        // Validate conditional monitoring fields ONLY if monitoring=Yes
        const monitoringYes = document.getElementById('monitoring_yes');
        if (monitoringYes && monitoringYes.checked) {
            const metersSelect = document.getElementById('num_digital_meters');
            if (!metersSelect.value) {
                const errorDiv = document.getElementById('error_num_digital_meters');
                if (errorDiv) {
                    errorDiv.textContent = 'Number of Digital Meters: Please select an option';
                    errorDiv.classList.add('show');
                }
                showError(metersSelect, errorDiv, 'Number of Digital Meters: Please select');
                errors.push({ id: 'num_digital_meters', label: 'Number of Digital Meters', message: 'Please select' });
                isValid = false;
            }

            const scadaChecked = form.querySelector('input[name="has_scada"]:checked');
            if (!scadaChecked) {
                const errorDiv = document.getElementById('error_has_scada');
                if (errorDiv) {
                    errorDiv.textContent = 'SCADA System: Please select an option';
                    errorDiv.classList.add('show');
                }
                errors.push({ id: 'error_has_scada', label: 'SCADA System', message: 'Please select an option' });
                isValid = false;
            }
        }
        // If monitoring=No, skip these fields entirely (no validation)

        // Validate "willing to participate" must be YES
        const participateYes = document.getElementById('participate_yes');
        const participateChecked = form.querySelector('input[name="willing_to_participate"]:checked');
        if (participateChecked && participateChecked.value !== 'yes') {
            const errorDiv = document.getElementById('error_willing_to_participate');
            if (errorDiv) {
                errorDiv.textContent = 'Participation: You must agree to participate free of charge to continue';
                errorDiv.classList.add('show');
            }
            errors.push({ id: 'error_willing_to_participate', label: 'Willing to Participate', message: 'Must be Yes' });
            isValid = false;
        }

        // Validate final confirmation checkbox
        const confirmCheckbox = document.getElementById('confirms_collaboration');
        if (!confirmCheckbox.checked) {
            const errorDiv = document.getElementById('error_confirms_collaboration');
            if (errorDiv) {
                errorDiv.textContent = 'Confirmation: You must confirm your willingness to collaborate';
                errorDiv.classList.add('show');
            }
            errors.push({ id: 'confirms_collaboration', label: 'Collaboration Confirmation', message: 'Must be checked' });
            isValid = false;
        }

        // If validation failed, show enhanced error UI
        if (!isValid) {
            markSectionErrors();
            showErrorSummary(errors);
            scrollToFirstError();
            announceErrors(errors.length);
        }

        return isValid;
    }

    function submitApplication() {
        // Show loading
        loadingOverlay.classList.add('show');
        submitButton.disabled = true;

        // Collect form data
        const formData = {
            company_name: getValue('company_name'),
            city_address: getValue('city_address'),
            contact_name: getValue('contact_name'),
            contact_position: getValue('contact_position'),
            contact_email: getValue('contact_email'),
            contact_phone: getValue('contact_phone'),
            company_website: getValue('company_website') || null,
            manufacturing_sector: getRadioValue('manufacturing_sector'),
            manufacturing_sector_other: getValue('manufacturing_sector_other') || null,
            num_employees: getRadioValue('num_employees'),
            facility_area: getRadioValue('facility_area'),
            annual_electricity: getRadioValue('annual_electricity'),
            num_production_operations: getRadioValue('num_production_operations'),
            digital_monitoring: getRadioValue('digital_monitoring') === 'yes' ? true : false,
            num_digital_meters: getValue('num_digital_meters') || null,
            has_scada: getRadioValue('has_scada') === 'yes' ? true : (getRadioValue('has_scada') === 'no' ? false : null),
            has_energy_responsible: getRadioValue('has_energy_responsible'),
            digital_maturity: getRadioValue('digital_maturity'),
            willing_to_participate: getRadioValue('willing_to_participate') === 'yes',
            preferred_meeting_week: getRadioValue('preferred_meeting_week') || null,
            preferred_installation_week: getRadioValue('preferred_installation_week') || null,
            confirms_collaboration: document.getElementById('confirms_collaboration').checked
        };

        // Send to API
        fetch('/api/auth/pilot-factory-apply', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw { status: response.status, data: data };
                });
            }
            return response.json();
        })
        .then(data => {
            // Success - store reference and redirect
            if (data.application_ref) {
                sessionStorage.setItem('pilot_app_ref', data.application_ref);
                sessionStorage.setItem('pilot_app_email', formData.contact_email);
                sessionStorage.setItem('pilot_app_company', formData.company_name);
            }
            
            // Redirect to thank you page
            window.location.href = '/pilot-factory-thank-you.html';
        })
        .catch(error => {
            console.error('Submission error:', error);
            loadingOverlay.classList.remove('show');
            submitButton.disabled = false;

            let errorMessage = 'An error occurred while submitting your application. Please try again.';

            if (error.status === 400) {
                errorMessage = error.data.message || 'Please check your form data and try again.';
            } else if (error.status === 409) {
                errorMessage = 'An application with this email address already exists. Please use a different email or contact us at bilgi@aartimuhendislik.com';
            } else if (error.status === 429) {
                errorMessage = 'Too many submission attempts. Please wait a few minutes before trying again.';
            } else if (error.status === 500) {
                errorMessage = 'Server error. Please try again later or contact us at bilgi@aartimuhendislik.com';
            }

            showMessage(errorMessage, 'error');
        });
    }

    // ==================== HELPER FUNCTIONS ====================

    function getValue(id) {
        const element = document.getElementById(id);
        return element ? element.value.trim() : '';
    }

    function getRadioValue(name) {
        const checked = form.querySelector(`input[name="${name}"]:checked`);
        return checked ? checked.value : null;
    }

    function showMessage(text, type) {
        messageBox.textContent = text;
        messageBox.className = 'message-box show ' + type;
        messageBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideMessage() {
        messageBox.classList.remove('show');
    }

    // ==================== ENHANCED ERROR UX FUNCTIONS ====================

    function clearErrorStyling() {
        // Remove all error classes
        document.querySelectorAll('.field-invalid').forEach(el => el.classList.remove('field-invalid'));
        document.querySelectorAll('.error-message.show').forEach(el => el.classList.remove('show'));
        document.querySelectorAll('.form-section.has-errors').forEach(el => el.classList.remove('has-errors'));
        document.querySelectorAll('.section-error-badge').forEach(badge => badge.remove());
        
        // Remove error summary
        const existingSummary = document.getElementById('error-summary');
        if (existingSummary) {
            existingSummary.remove();
        }
    }

    function markSectionErrors() {
        // Remove existing error badges
        document.querySelectorAll('.section-error-badge').forEach(badge => badge.remove());
        document.querySelectorAll('.form-section').forEach(section => section.classList.remove('has-errors'));
        
        // Find sections with errors
        const sections = document.querySelectorAll('.form-section');
        sections.forEach(section => {
            const invalidFields = section.querySelectorAll('.field-invalid');
            const errorMessages = section.querySelectorAll('.error-message.show');
            
            const errorCount = invalidFields.length + errorMessages.length;
            if (errorCount > 0) {
                section.classList.add('has-errors');
                
                const badge = document.createElement('div');
                badge.className = 'section-error-badge';
                badge.textContent = `${errorCount} error${errorCount > 1 ? 's' : ''}`;
                section.style.position = 'relative';
                
                // Insert badge after section title
                const sectionTitle = section.querySelector('.section-title');
                if (sectionTitle) {
                    sectionTitle.parentNode.insertBefore(badge, sectionTitle.nextSibling);
                } else {
                    section.insertBefore(badge, section.firstChild);
                }
            }
        });
    }

    function showErrorSummary(errors) {
        const container = document.getElementById('error-summary-container');
        if (!container) return;
        
        const existingSummary = document.getElementById('error-summary');
        if (existingSummary) {
            existingSummary.remove();
        }
        
        const summary = document.createElement('div');
        summary.id = 'error-summary';
        summary.className = 'error-summary';
        
        summary.innerHTML = `
            <h3>⚠️ ${errors.length} field${errors.length > 1 ? 's' : ''} require${errors.length === 1 ? 's' : ''} your attention</h3>
            <ul>
                ${errors.map(err => `
                    <li>
                        <a href="#${err.id}" data-field-id="${err.id}">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <strong>${err.label}:</strong> ${err.message}
                        </a>
                    </li>
                `).join('')}
            </ul>
            <button onclick="document.getElementById('error-summary').remove();">Dismiss</button>
        `;
        
        container.appendChild(summary);
        
        // Add click handlers to error links
        summary.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const fieldId = this.getAttribute('data-field-id');
                scrollToField(fieldId);
            });
        });
        
        // Scroll to summary
        summary.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function scrollToFirstError() {
        const firstError = document.querySelector('.field-invalid, .has-errors .error-message.show');
        if (firstError) {
            // Scroll with offset for sticky header
            const elementPosition = firstError.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - 100;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
            
            // Focus first invalid input if it's an input element
            const firstInvalidInput = document.querySelector('.field-invalid');
            if (firstInvalidInput && (firstInvalidInput.tagName === 'INPUT' || firstInvalidInput.tagName === 'SELECT' || firstInvalidInput.tagName === 'TEXTAREA')) {
                setTimeout(() => {
                    firstInvalidInput.focus();
                }, 600);
            }
        }
    }

    function scrollToField(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            const elementPosition = field.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - 100;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            setTimeout(() => {
                if (field.tagName === 'INPUT' || field.tagName === 'SELECT' || field.tagName === 'TEXTAREA') {
                    field.focus();
                }
            }, 600);
        }
    }

    function announceErrors(errorCount) {
        const announcement = document.getElementById('error-announcement');
        if (announcement) {
            announcement.textContent = `Please correct ${errorCount} error${errorCount > 1 ? 's' : ''} in the form`;
        }
    }

    // ==================== MAKE RADIO/CHECKBOX OPTIONS FULLY CLICKABLE ====================

    function makeRadioOptionsClickable() {
        // Make entire radio option div clickable
        const radioOptions = document.querySelectorAll('.radio-option');
        radioOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                // Don't trigger if clicking on the input itself (already handled)
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'LABEL') {
                    return;
                }
                
                // Find the radio input inside this option
                const radio = this.querySelector('input[type="radio"]');
                if (radio && !radio.disabled) {
                    radio.checked = true;
                    // Trigger change event for conditional field logic
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        });

        // Make entire checkbox option div clickable
        const checkboxOptions = document.querySelectorAll('.checkbox-option');
        checkboxOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                // Don't trigger if clicking on the input itself (already handled)
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'LABEL') {
                    return;
                }
                
                // Find the checkbox input inside this option
                const checkbox = this.querySelector('input[type="checkbox"]');
                if (checkbox && !checkbox.disabled) {
                    checkbox.checked = !checkbox.checked;
                    // Trigger change event
                    checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        });
    }

})();
