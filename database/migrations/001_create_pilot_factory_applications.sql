-- ============================================================================
-- Pilot Factory Applications Database Schema
-- Created: January 2, 2026
-- Purpose: Store pilot factory applications for HumanEnerDIA WASABI Project
-- ============================================================================

-- Create pilot_factory_applications table
CREATE TABLE IF NOT EXISTS public.pilot_factory_applications (
    id SERIAL PRIMARY KEY,
    
    -- Application Reference (unique identifier)
    application_ref VARCHAR(20) UNIQUE NOT NULL,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL,
    city_address TEXT NOT NULL,
    company_website VARCHAR(255),
    
    -- Contact Information
    contact_name VARCHAR(255) NOT NULL,
    contact_position VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(50) NOT NULL,
    
    -- Factory Profile
    manufacturing_sector VARCHAR(100) NOT NULL,
    manufacturing_sector_other VARCHAR(255),
    num_employees VARCHAR(50) NOT NULL,
    facility_area VARCHAR(50) NOT NULL,
    annual_electricity VARCHAR(50) NOT NULL,
    num_production_operations VARCHAR(50) NOT NULL,
    
    -- Digital & Energy Readiness
    digital_monitoring BOOLEAN NOT NULL,
    num_digital_meters VARCHAR(50),
    has_scada BOOLEAN,
    has_energy_responsible VARCHAR(50) NOT NULL,
    digital_maturity VARCHAR(50) NOT NULL,
    
    -- Participation Conditions
    willing_to_participate BOOLEAN NOT NULL,
    
    -- Availability
    preferred_meeting_week VARCHAR(50),
    preferred_installation_week VARCHAR(50),
    
    -- Confirmation
    confirms_collaboration BOOLEAN NOT NULL,
    
    -- Admin Management
    status VARCHAR(50) DEFAULT 'pending',
    admin_notes TEXT,
    
    -- Tracking & Audit
    ip_address VARCHAR(50),
    user_agent TEXT,
    
    -- Timestamps
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    reviewed_by INTEGER REFERENCES public.demo_users(id),
    
    -- Constraints
    CONSTRAINT email_lowercase CHECK (contact_email = LOWER(contact_email))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_pilot_applications_ref ON public.pilot_factory_applications(application_ref);
CREATE INDEX IF NOT EXISTS idx_pilot_applications_email ON public.pilot_factory_applications(contact_email);
CREATE INDEX IF NOT EXISTS idx_pilot_applications_status ON public.pilot_factory_applications(status);
CREATE INDEX IF NOT EXISTS idx_pilot_applications_submitted_at ON public.pilot_factory_applications(submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_pilot_applications_company_name ON public.pilot_factory_applications(company_name);

-- Trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_pilot_applications_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_pilot_applications_updated_at
    BEFORE UPDATE ON public.pilot_factory_applications
    FOR EACH ROW
    EXECUTE FUNCTION update_pilot_applications_updated_at();

-- ============================================================================
-- Comments for documentation
-- ============================================================================
COMMENT ON TABLE public.pilot_factory_applications IS 'Stores pilot factory applications for HumanEnerDIA WASABI Project field trials';
COMMENT ON COLUMN public.pilot_factory_applications.application_ref IS 'Unique application reference number (format: PF2026-XXXX)';
COMMENT ON COLUMN public.pilot_factory_applications.status IS 'Application status: pending, under_review, reviewed, accepted, rejected';
COMMENT ON COLUMN public.pilot_factory_applications.ip_address IS 'IP address of submission for fraud detection';
COMMENT ON COLUMN public.pilot_factory_applications.user_agent IS 'Browser user agent for tracking';

-- ============================================================================
-- Test the schema (commented out - uncomment to test)
-- ============================================================================
-- INSERT INTO public.pilot_factory_applications (
--     application_ref, company_name, city_address, contact_name, contact_position,
--     contact_email, contact_phone, manufacturing_sector, num_employees,
--     facility_area, annual_electricity, num_production_operations,
--     digital_monitoring, has_energy_responsible, digital_maturity,
--     willing_to_participate, confirms_collaboration
-- ) VALUES (
--     'PF2026-0001', 'Test Factory Ltd', 'Bucharest, Romania', 'John Doe', 'Energy Manager',
--     'test@example.com', '+40123456789', 'Electronics', '50-149',
--     '2000-10000', '200-500 MWh', '5-8',
--     true, 'Yes, already have', 'Medium',
--     true, true
-- );
--
-- SELECT * FROM public.pilot_factory_applications;

-- ============================================================================
-- Cleanup (if needed)
-- ============================================================================
-- DROP TRIGGER IF EXISTS trigger_pilot_applications_updated_at ON public.pilot_factory_applications;
-- DROP FUNCTION IF EXISTS update_pilot_applications_updated_at();
-- DROP TABLE IF EXISTS public.pilot_factory_applications CASCADE;
