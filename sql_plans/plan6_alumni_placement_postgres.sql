-- ============================================================================
-- PLAN 6: ALUMNI & PLACEMENT (14 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 6.1 COLLEGE_ALUMNI_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_records (
    id BIGSERIAL PRIMARY KEY,
    alumni_number VARCHAR(50) UNIQUE NOT NULL,
    student_id BIGINT UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_primary VARCHAR(20),
    phone_secondary VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(50),
    blood_group VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    graduation_year INT NOT NULL,
    graduation_month VARCHAR(10) DEFAULT 'may' CHECK (graduation_month IN ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')),
    degree_type VARCHAR(50) NOT NULL CHECK (degree_type IN ('bachelor', 'master', 'diploma', 'certificate', 'phd')),
    department_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    specialization VARCHAR(255),
    roll_number VARCHAR(100),
    cgpa DECIMAL(4,2),
    division VARCHAR(10),
    current_job_title VARCHAR(255),
    current_company VARCHAR(255),
    industry_sector VARCHAR(255),
    job_type VARCHAR(50) DEFAULT 'full_time' CHECK (job_type IN ('full_time', 'part_time', 'freelance', 'self_employed', 'unemployed', 'studying')),
    experience_years DECIMAL(4,1) DEFAULT 0.0,
    current_salary DECIMAL(14,2),
    salary_currency VARCHAR(3) DEFAULT 'INR',
    current_city VARCHAR(100),
    current_state VARCHAR(100),
    current_country VARCHAR(100) DEFAULT 'India',
    linkedin_url TEXT,
    facebook_url TEXT,
    twitter_handle VARCHAR(100),
    website_portfolio TEXT,
    skills JSONB,
    certifications JSONB,
    languages_known JSONB,
    is_visible_in_directory BOOLEAN DEFAULT TRUE,
    is_willing_to_mentor BOOLEAN DEFAULT FALSE,
    is_willing_to_hire BOOLEAN DEFAULT FALSE,
    wants_job_alerts BOOLEAN DEFAULT TRUE,
    newsletter_subscription BOOLEAN DEFAULT TRUE,
    last_contacted_date DATE,
    last_contact_method VARCHAR(50),
    engagement_score INT DEFAULT 0 CHECK (engagement_score BETWEEN 0 AND 100),
    notes TEXT,
    data_source VARCHAR(50) DEFAULT 'student_record' CHECK (data_source IN ('student_record', 'self_registered', 'linkedin_import', 'manual')),
    profile_complete_percentage INT DEFAULT 0,
    last_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alumni_number ON college_alumni_records(alumni_number);
CREATE INDEX idx_student ON college_alumni_records(student_id);
CREATE INDEX idx_graduation ON college_alumni_records(graduation_year, department_id);
CREATE INDEX idx_dept_course ON college_alumni_records(department_id, course_id);
CREATE INDEX idx_email ON college_alumni_records(email);
CREATE INDEX idx_location ON college_alumni_records(current_city, current_state, current_country);
CREATE INDEX idx_company ON college_alumni_records(current_company);
CREATE INDEX idx_skills ON college_alumni_records USING GIN (skills);
CREATE INDEX idx_engagement ON college_alumni_records(engagement_score);
CREATE INDEX idx_mentor ON college_alumni_records(is_willing_to_mentor);
CREATE INDEX idx_visible ON college_alumni_records(is_visible_in_directory);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_search ON college_alumni_records USING GIN (to_tsvector('english', first_name || ' ' || last_name || ' ' || COALESCE(current_company, '') || ' ' || COALESCE(current_job_title, '') || ' ' || COALESCE(skills::text, '')));

ALTER TABLE college_alumni_records
    ADD CONSTRAINT fk_alumni_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_alumni_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_alumni_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 6.2 COLLEGE_ALUMNI_EVENTS
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_events (
    id BIGSERIAL PRIMARY KEY,
    event_code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) DEFAULT 'reunion' CHECK (event_type IN ('reunion', 'networking', 'workshop', 'panel_discussion', 'job_fair', 'fundraising', 'other')),
    venue VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    event_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    is_virtual BOOLEAN DEFAULT FALSE,
    virtual_meeting_url TEXT,
    registration_required BOOLEAN DEFAULT TRUE,
    registration_deadline DATE,
    max_participants INT,
    current_registrations INT DEFAULT 0,
    fee_amount DECIMAL(10,2) DEFAULT 0.00,
    organizer_team JSONB,
    host_department_id BIGINT,
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    sponsor_details JSONB,
    agenda JSONB,
    attachments JSONB,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_event_code ON college_alumni_events(event_code);
CREATE INDEX idx_event_dates ON college_alumni_events(event_date, registration_deadline);
CREATE INDEX idx_event_type ON college_alumni_events(event_type);
CREATE INDEX idx_published ON college_alumni_events(is_published);
CREATE INDEX_idx_department ON college_alumni_events(host_department_id);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_event_search ON college_alumni_events USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));

ALTER TABLE college_alumni_events
    ADD CONSTRAINT fk_event_department FOREIGN KEY (host_department_id) REFERENCES college_departments(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_event_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_end_after_start CHECK (end_time IS NULL OR end_time >= start_time);

-- -----------------------------------------------------------------------------
-- 6.3 COLLEGE_ALUMNI_EVENT_ATTENDEES
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_event_attendees (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL,
    attendee_type VARCHAR(20) DEFAULT 'alumni' CHECK (attendee_type IN ('alumni', 'student', 'faculty', 'guest', 'speaker', 'sponsor')),
    attendee_id BIGINT,
    registration_number VARCHAR(50) UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attendance_status VARCHAR(20) DEFAULT 'registered' CHECK (attendance_status IN ('registered', 'confirmed', 'attended', 'cancelled', 'no_show')),
    checkin_time TIME,
    checkout_time TIME,
    certificate_issued BOOLEAN DEFAULT FALSE,
    certificate_url TEXT,
    feedback_submitted BOOLEAN DEFAULT FALSE,
    feedback_id BIGINT,
    special_requirements TEXT,
    dietary_restrictions JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_event_attendees_event ON college_alumni_event_attendees(event_id);
CREATE INDEX idx_attendee ON college_alumni_event_attendees(attendee_type, attendee_id);
CREATE INDEX idx_status ON college_alumni_event_attendees(attendance_status);
CREATE INDEX idx_certificate ON college_alumni_event_attendees(certificate_issued);

ALTER TABLE college_alumni_event_attendees
    ADD CONSTRAINT fk_event_attendee_event FOREIGN KEY (event_id) REFERENCES college_alumni_events(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_event_feedback FOREIGN KEY (feedback_id) REFERENCES college_alumni_feedback(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 6.4 COLLEGE_ALUMNI_DONATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_donations (
    id BIGSERIAL PRIMARY KEY,
    donation_number VARCHAR(50) UNIQUE NOT NULL,
    donor_id BIGINT NOT NULL,
    donation_type VARCHAR(50) DEFAULT 'one_time' CHECK (donation_type IN ('one_time', 'recurring', 'scholarship', 'infrastructure', 'research', 'other')),
    amount DECIMAL(14,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    donation_date DATE NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'online_transfer' CHECK (payment_method IN ('cash', 'cheque', 'card', 'online_transfer', 'upi', 'foreign_transfer')),
    transaction_reference VARCHAR(255) UNIQUE,
    bank_name VARCHAR(255),
    cheque_number VARCHAR(100),
    cheque_date DATE,
    receipt_issued BOOLEAN DEFAULT FALSE,
    receipt_number VARCHAR(100),
    receipt_date DATE,
    tax_benefit_eligible BOOLEAN DEFAULT FALSE,
    tax_exemption_certificate_sent BOOLEAN DEFAULT FALSE,
    dedication TEXT,
    restricted_to_department BIGINT,
    restricted_to_course BIGINT,
    is_anonymous BOOLEAN DEFAULT FALSE,
    gift_matching_company VARCHAR(255),
    installment_count INT DEFAULT 1,
    installment_frequency VARCHAR(20),
    next_installment_date DATE,
    campaign_id BIGINT,
    notes TEXT,
    receipt_generated_at TIMESTAMP,
    receipt_generated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_donation_number ON college_alumni_donations(donation_number);
CREATE INDEX idx_donor ON college_alumni_donations(donor_id);
CREATE INDEX idx_donation_date ON college_alumni_donations(donation_date);
CREATE INDEX idx_donation_type ON college_alumni_donations(donation_type);
CREATE INDEX idx_receipt ON college_alumni_donations(receipt_number);
CREATE INDEX idx_anonymous ON college_alumni_donations(is_anonymous);
CREATE INDEX idx_campaign ON college_alumni_donations(campaign_id);

ALTER TABLE college_alumni_donations
    ADD CONSTRAINT fk_donation_donor FOREIGN KEY (donor_id) REFERENCES college_alumni_records(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_restricted_department FOREIGN KEY (restricted_to_department) REFERENCES college_departments(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_restricted_course FOREIGN KEY (restricted_to_course) REFERENCES college_courses(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_receipt_generated_by FOREIGN KEY (receipt_generated_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_amount_positive CHECK (amount > 0),
    ADD CONSTRAINT chk_installment_count CHECK (installment_count >= 1);

-- -----------------------------------------------------------------------------
-- 6.5 COLLEGE_ALUMNI_MENTORSHIP
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_mentorship (
    id BIGSERIAL PRIMARY KEY,
    mentor_alumni_id BIGINT NOT NULL,
    mentee_type VARCHAR(20) DEFAULT 'student' CHECK (mentee_type IN ('student', 'junior_alumni')),
    mentee_id BIGINT,
    mentorship_program_id BIGINT,
    start_date DATE NOT NULL,
    end_date DATE,
    expected_end_date DATE,
    frequency VARCHAR(20) DEFAULT 'monthly' CHECK (frequency IN ('weekly', 'biweekly', 'monthly', 'ad_hoc')),
    preferred_contact_mode VARCHAR(50) DEFAULT 'email' CHECK (preferred_contact_mode IN ('email', 'phone', 'video_call', 'in_person')),
    mentor_availability JSONB,
    mentorship_goals JSONB,
    progress_notes TEXT,
    last_contact_date DATE,
    next_meeting_scheduled DATE,
    mentor_satisfaction_rating INT,
    mentee_satisfaction_rating INT,
    status VARCHAR(20) DEFAULT 'matched' CHECK (status IN ('active', 'completed', 'paused', 'terminated', 'matched')),
    termination_reason TEXT,
    terminated_by BIGINT,
    mentor_agreed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mentor_agreed_ip INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mentor ON college_alumni_mentorship(mentor_alumni_id);
CREATE INDEX idx_mentee ON college_alumni_mentorship(mentee_type, mentee_id);
CREATE INDEX idx_mentorship_status ON college_alumni_mentorship(status);
CREATE INDEX idx_mentorship_program ON college_alumni_mentorship(mentorship_program_id);
CREATE INDEX idx_dates ON college_alumni_mentorship(start_date, end_date);

ALTER TABLE college_alumni_mentorship
    ADD CONSTRAINT fk_mentor FOREIGN KEY (mentor_alumni_id) REFERENCES college_alumni_records(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_mentee FOREIGN KEY (mentee_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_terminated_by FOREIGN KEY (terminated_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_end_after_start CHECK (end_date IS NULL OR end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 6.6 COLLEGE_ALUMNI_EMPLOYMENT
-- -----------------------------------------------------------------------------
CREATE TABLE college_alumni_employment (
    id BIGSERIAL PRIMARY KEY,
    alumni_id BIGINT NOT NULL,
    employer_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    employment_type VARCHAR(50) DEFAULT 'full_time' CHECK (employment_type IN ('full_time', 'part_time', 'contract', 'internship', 'freelance', 'self_employed')),
    industry_sector VARCHAR(255),
    job_function VARCHAR(255),
    location_city VARCHAR(100),
    location_state VARCHAR(100),
    location_country VARCHAR(100) DEFAULT 'India',
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    salary_band VARCHAR(50),
    responsibilities TEXT,
    achievements TEXT,
    skills_used JSONB,
    company_size VARCHAR(50),
    company_type VARCHAR(50),
    reporting_manager VARCHAR(255),
    company_website TEXT,
    verified BOOLEAN DEFAULT FALSE,
    verified_by BIGINT,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alumni_emp ON college_alumni_employment(alumni_id);
CREATE INDEX idx_employer ON college_alumni_employment(employer_name);
CREATE INDEX idx_current_job ON college_alumni_employment(is_current);
CREATE INDEX idx_emp_dates ON college_alumni_employment(start_date, end_date);
CREATE INDEX idx_industry ON college_alumni_employment(industry_sector);

ALTER TABLE college_alumni_employment
    ADD CONSTRAINT fk_emp_alumni FOREIGN KEY (alumni_id) REFERENCES college_alumni_records(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_end_after_start CHECK (end_date IS NULL OR end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 6.7 COLLEGE_INDUSTRY_PARTNERS
-- -----------------------------------------------------------------------------
CREATE TABLE college_industry_partners (
    id BIGSERIAL PRIMARY KEY,
    partner_code VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(500),
    industry_sector VARCHAR(255),
    company_size VARCHAR(50),
    company_type VARCHAR(50),
    contact_person_name VARCHAR(255),
    contact_designation VARCHAR(100),
    contact_email VARCHAR(255) UNIQUE,
    contact_phone_primary VARCHAR(20),
    contact_phone_secondary VARCHAR(20),
    website_url TEXT,
    linkedin_company_url TEXT,
    hrd_email VARCHAR(255),
    hrd_phone VARCHAR(20),
    address_line1 TEXT,
    address_line2 TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    country VARCHAR(100) DEFAULT 'India',
    gst_number VARCHAR(50),
    pan_number VARCHAR(50),
    partnership_level VARCHAR(50) DEFAULT 'associate' CHECK (partnership_level IN ('platinum', 'gold', 'silver', 'bronze', 'associate')),
    partnership_start_date DATE,
    partnership_end_date DATE,
    total_mou_signed INT DEFAULT 0,
    active_mou_count INT DEFAULT 0,
    last_campus_visit_date DATE,
    offers_extended_count INT DEFAULT 0,
    offers_accepted_count INT DEFAULT 0,
    placement_conversion_rate DECIMAL(5,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured_partner BOOLEAN DEFAULT FALSE,
    logo_url TEXT,
    description TEXT,
    tags JSONB,
    company_culture_rating INT,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_partner_code ON college_industry_partners(partner_code);
CREATE INDEX idx_company ON college_industry_partners(company_name);
CREATE INDEX idx_sector ON college_industry_partners(industry_sector);
CREATE INDEX idx_level ON college_industry_partners(partnership_level);
CREATE INDEX idx_contact ON college_industry_partners(contact_email, contact_phone_primary);
CREATE INDEX idx_partner_active ON college_industry_partners(is_active);
CREATE INDEX idx_featured ON college_industry_partners(is_featured_partner);
CREATE INDEX idx_tags ON college_industry_partners USING GIN (tags);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_partner_search ON college_industry_partners USING GIN (to_tsvector('english', company_name || ' ' || COALESCE(description, '') || ' ' || COALESCE(industry_sector, '') || ' ' || COALESCE(tags::text, '')));

ALTER TABLE college_industry_partners
    ADD CONSTRAINT fk_partner_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 6.8 COLLEGE_INTERNSHIPS
-- -----------------------------------------------------------------------------
CREATE TABLE college_internships (
    id BIGSERIAL PRIMARY KEY,
    internship_code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    company_id BIGINT NOT NULL,
    industry_sector VARCHAR(255),
    job_function VARCHAR(255),
    location_type VARCHAR(50) DEFAULT 'on_site' CHECK (location_type IN ('on_site', 'remote', 'hybrid')),
    location_city VARCHAR(100),
    location_state VARCHAR(100),
    work_from_home_possible BOOLEAN DEFAULT FALSE,
    internship_type VARCHAR(50) DEFAULT 'summer' CHECK (internship_type IN ('summer', 'winter', 'semester', 'year_long', 'project_based')),
    duration_months DECIMAL(4,1) NOT NULL CHECK (duration_months > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    stipend_amount DECIMAL(10,2),
    stipend_frequency VARCHAR(20) DEFAULT 'monthly' CHECK (stipend_frequency IN ('monthly', 'weekly', 'lump_sum', 'unpaid')),
    stipend_currency VARCHAR(3) DEFAULT 'INR',
    eligibility_branch JSONB,
    eligibility_min_cgpa DECIMAL(4,2),
    eligibility_semester_min INT,
    eligibility_semester_max INT,
    required_skills JSONB,
    preferred_skills JSONB,
    selection_process JSONB,
    application_deadline DATE,
    posting_date DATE,
    total_openings INT DEFAULT 1,
    filled_count INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'closed', 'filled', 'cancelled')),
    is_featured BOOLEAN DEFAULT FALSE,
    featured_until DATE,
    attachment_urls JSONB,
    posted_by BIGINT NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_internship_code ON college_internships(internship_code);
CREATE INDEX idx_company ON college_internships(company_id);
CREATE INDEX idx_dates ON college_internships(start_date, end_date);
CREATE INDEX idx_deadline ON college_internships(application_deadline);
CREATE INDEX idx_status ON college_internships(status);
CREATE INDEX idx_featured ON college_internships(is_featured, featured_until);
CREATE INDEX idx_type_location ON college_internships(internship_type, location_type, location_city);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_internship_search ON college_internships USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '') || ' ' || COALESCE(required_skills::text, '')));

ALTER TABLE college_internships
    ADD CONSTRAINT fk_internship_company FOREIGN KEY (company_id) REFERENCES college_industry_partners(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_posted_by FOREIGN KEY (posted_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_dates CHECK (end_date > start_date),
    ADD CONSTRAINT chk_filled_count CHECK (filled_count <= total_openings);

-- -----------------------------------------------------------------------------
-- 6.9 COLLEGE_INTERNSHIP_APPLICATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_internship_applications (
    id BIGSERIAL PRIMARY KEY,
    internship_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    application_number VARCHAR(50) UNIQUE NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'applied' CHECK (status IN ('applied', 'shortlisted', 'interview_scheduled', 'selected', 'rejected', 'withdrawn', 'offer_declined')),
    resume_url TEXT NOT NULL,
    cover_letter TEXT,
    current_semester INT,
    expected_graduation_date DATE,
    gpa DECIMAL(4,2),
    relevant_experience TEXT,
    why_interested TEXT,
    availability_start_date DATE,
    availability_end_date DATE,
    interviewer_ratings JSONB,
    interview_feedback TEXT,
    interview_date DATE,
    interview_time TIME,
    interview_panel_json JSONB,
    selected_for_another_internship BOOLEAN DEFAULT FALSE,
    other_offer_company VARCHAR(255),
    offer_received_date DATE,
    offer_accepted BOOLEAN DEFAULT FALSE,
    offer_accepted_date DATE,
    expected_stipend DECIMAL(10,2),
    negotiation_notes TEXT,
    notes_internal TEXT,
    applied_through VARCHAR(50) DEFAULT 'portal' CHECK (applied_through IN ('portal', 'referral', 'company_website', 'event', 'other')),
    referral_alumni_id BIGINT,
    referral_bonus_eligible BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_app_number ON college_internship_applications(application_number);
CREATE INDEX idx_internship_student ON college_internship_applications(internship_id, student_id);
CREATE INDEX idx_student_status ON college_internship_applications(student_id, status);
CREATE INDEX idx_app_status ON college_internship_applications(status);
CREATE INDEX idx_interview ON college_internship_applications(interview_date);
CREATE INDEX idx_offer ON college_internship_applications(offer_received_date, offer_accepted);
CREATE INDEX idx_referral ON college_internship_applications(referral_alumni_id);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_app_search ON college_internship_applications USING GIN (to_tsvector('english', COALESCE(cover_letter, '') || ' ' || COALESCE(relevant_experience, '') || ' ' || COALESCE(why_interested, '')));

ALTER TABLE college_internship_applications
    ADD CONSTRAINT fk_app_internship FOREIGN KEY (internship_id) REFERENCES college_internships(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_app_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_referral_alumni FOREIGN KEY (referral_alumni_id) REFERENCES college_alumni_records(id) ON DELETE SET NULL,
    ADD CONSTRAINT uk_internship_student UNIQUE (internship_id, student_id);

-- -----------------------------------------------------------------------------
-- 6.10 COLLEGE_INTERNSHIP_EVALUATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_internship_evaluations (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT UNIQUE NOT NULL,
    evaluated_by BIGINT NOT NULL,
    technical_skills_rating INT CHECK (technical_skills_rating BETWEEN 1 AND 10),
    professional_conduct_rating INT CHECK (professional_conduct_rating BETWEEN 1 AND 10),
    punctuality_rating INT CHECK (punctuality_rating BETWEEN 1 AND 10),
    communication_rating INT CHECK (communication_rating BETWEEN 1 AND 10),
    task_completion_rating INT CHECK (task_completion_rating BETWEEN 1 AND 10),
    overall_rating DECIMAL(4,2) GENERATED ALWAYS AS (
        (technical_skills_rating + professional_conduct_rating + punctuality_rating + communication_rating + task_completion_rating) / 5.0
    ) STORED,
    supervisor_feedback TEXT,
    student_self_evaluation TEXT,
    project_deliverables JSONB,
    skills_acquired JSONB,
    hours_worked INT,
    days_present INT,
    recommendation_letter_sent BOOLEAN DEFAULT FALSE,
    recommendation_letter_url TEXT,
    is_eligible_for_credit BOOLEAN DEFAULT FALSE,
    credit_hours_awarded INT,
    evaluation_completed BOOLEAN DEFAULT FALSE,
    evaluation_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_eval_application ON college_internship_evaluations(application_id);
CREATE INDEX idx_evaluator ON college_internship_evaluations(evaluated_by);
CREATE INDEX idx_rating ON college_internship_evaluations(overall_rating);

ALTER TABLE college_internship_evaluations
    ADD CONSTRAINT fk_eval_application FOREIGN KEY (application_id) REFERENCES college_internship_applications(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_evaluated_by FOREIGN KEY (evaluated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 6.11 COLLEGE_PLACEMENT_DRIVES
-- -----------------------------------------------------------------------------
CREATE TABLE college_placement_drives (
    id BIGSERIAL PRIMARY KEY,
    drive_code VARCHAR(50) UNIQUE NOT NULL,
    company_id BIGINT NOT NULL,
    drive_title VARCHAR(500) NOT NULL,
    job_profile VARCHAR(255) NOT NULL,
    description TEXT,
    job_location_type VARCHAR(50) DEFAULT 'on_site' CHECK (job_location_type IN ('on_site', 'remote', 'hybrid')),
    job_location_cities JSONB,
    job_department VARCHAR(255),
    job_band VARCHAR(100),
    package_components JSONB,
    ctc_min DECIMAL(14,2),
    ctc_max DECIMAL(14,2),
    ctc_currency VARCHAR(3) DEFAULT 'INR',
    eligibility_cgpa_min DECIMAL(4,2),
    eligibility_backlogs_allowed INT DEFAULT 0,
    eligibility_branches JSONB,
    eligibility_semester_min INT,
    eligibility_semester_max INT,
    selection_process JSONB,
    rounds_details JSONB,
    application_deadline DATE,
    drive_date DATE NOT NULL,
    drive_start_time TIME,
    drive_end_time TIME,
    venue VARCHAR(500),
    is_virtual BOOLEAN DEFAULT FALSE,
    virtual_meeting_url TEXT,
    registration_required BOOLEAN DEFAULT TRUE,
    max_registrations INT,
    current_registrations INT DEFAULT 0,
    offers_extended INT DEFAULT 0,
    offers_accepted INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'registration_open', 'in_progress', 'completed', 'cancelled')),
    drive_coordinator_id BIGINT,
    placement_officer_id BIGINT,
    company_hr_contacts JSONB,
    company_representatives JSONB,
    is_featured BOOLEAN DEFAULT FALSE,
    attachment_urls JSONB,
    remarks TEXT,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drive_code ON college_placement_drives(drive_code);
CREATE INDEX idx_company ON college_placement_drives(company_id);
CREATE INDEX idx_drive_dates ON college_placement_drives(drive_date, application_deadline);
CREATE INDEX idx_drive_status ON college_placement_drives(status);
CREATE INDEX idx_registrations ON college_placement_drives(current_registrations, max_registrations);
CREATE INDEX idx_featured ON college_placement_drives(is_featured);

ALTER TABLE college_placement_drives
    ADD CONSTRAINT fk_drive_company FOREIGN KEY (company_id) REFERENCES college_industry_partners(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_drive_coordinator FOREIGN KEY (drive_coordinator_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_placement_officer FOREIGN KEY (placement_officer_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 6.12 COLLEGE_PLACEMENT_APPLICATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_placement_applications (
    id BIGSERIAL PRIMARY KEY,
    drive_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    application_number VARCHAR(50) UNIQUE NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'applied' CHECK (status IN ('applied', 'shortlisted_test', 'shortlisted_interview', 'selected', 'rejected', 'offer_extended', 'offer_accepted', 'offer_declined', 'withdrawn')),
    resume_url TEXT NOT NULL,
    applied_for_profile VARCHAR(255),
    expected_ctc DECIMAL(14,2),
    resume_shortlisted BOOLEAN DEFAULT FALSE,
    shortlisted_at TIMESTAMP,
    shortlisted_by BIGINT,
    test_round_cleared BOOLEAN DEFAULT FALSE,
    test_score DECIMAL(6,2),
    test_rank INT,
    interview_round_cleared BOOLEAN DEFAULT FALSE,
    interview_feedback TEXT,
    interviewer_ratings JSONB,
    final_verdict VARCHAR(50),
    offer_letter_url TEXT,
    offer_letter_date DATE,
    offer_validity_date DATE,
    offered_ctc DECIMAL(14,2),
    offered_currency VARCHAR(3) DEFAULT 'INR',
    offer_accepted BOOLEAN DEFAULT FALSE,
    offer_accepted_date DATE,
    joining_date DATE,
    actual_ctc DECIMAL(14,2),
    actual_currency VARCHAR(3),
    feedback_from_company TEXT,
    student_feedback TEXT,
    placement_remarks_internal TEXT,
    applied_through VARCHAR(50) DEFAULT 'campus' CHECK (applied_through IN ('direct', 'referral', 'campus', 'alumni_referral')),
    referral_by_alumni_id BIGINT,
    pre_placement_training_completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_placement_app_number ON college_placement_applications(application_number);
CREATE INDEX idx_drive_student ON college_placement_applications(drive_id, student_id);
CREATE INDEX idx_student_placement_status ON college_placement_applications(student_id, status);
CREATE INDEX idx_placement_status ON college_placement_applications(status);
CREATE INDEX idx_drive_status ON college_placement_applications(drive_id, status);
CREATE INDEX idx_offer ON college_placement_applications(offer_letter_date, offer_accepted);
CREATE INDEX idx_joining ON college_placement_applications(joining_date);
CREATE INDEX idx_placement_referral ON college_placement_applications(referral_by_alumni_id);

ALTER TABLE college_placement_applications
    ADD CONSTRAINT fk_placement_drive FOREIGN KEY (drive_id) REFERENCES college_placement_drives(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_placement_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_referral_alumni FOREIGN KEY (referral_by_alumni_id) REFERENCES college_alumni_records(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_shortlisted_by FOREIGN KEY (shortlisted_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT uk_drive_student UNIQUE (drive_id, student_id);

-- -----------------------------------------------------------------------------
-- 6.13 COLLEGE_PLACEMENT_OFFERS
-- -----------------------------------------------------------------------------
CREATE TABLE college_placement_offers (
    id BIGSERIAL PRIMARY KEY,
    offer_number VARCHAR(50) UNIQUE NOT NULL,
    application_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    company_id BIGINT NOT NULL,
    job_profile VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    location_city VARCHAR(100),
    location_state VARCHAR(100),
    ctc_offered DECIMAL(14,2) NOT NULL,
    ctc_currency VARCHAR(3) DEFAULT 'INR',
    gross_salary DECIMAL(14,2),
    fixed_component DECIMAL(14,2),
    variable_component DECIMAL(14,2),
    joining_bonus DECIMAL(14,2),
    stock_options BOOLEAN DEFAULT FALSE,
    other_benefits JSONB,
    joining_date DATE NOT NULL,
    probation_period_months INT DEFAULT 6,
    reporting_manager VARCHAR(255),
    hr_contact_email VARCHAR(255),
    hr_contact_phone VARCHAR(20),
    offer_letter_url TEXT,
    offer_letter_sent_date DATE,
    student_response_date DATE,
    student_response VARCHAR(50) DEFAULT 'no_response' CHECK (student_response IN ('accepted', 'declined', 'negotiating', 'no_response')),
    decline_reason TEXT,
    negotiation_notes TEXT,
    final_ctc DECIMAL(14,2),
    status VARCHAR(50) DEFAULT 'offered' CHECK (status IN ('offered', 'accepted', 'declined', 'withdrawn', 'joined', 'no_show')),
    placement_officer_id BIGINT,
    approval_status VARCHAR(50) DEFAULT 'approved' CHECK (approval_status IN ('pending', 'approved', 'rejected')),
    approved_by BIGINT,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_offer_number ON college_placement_offers(offer_number);
CREATE INDEX idx_offer_application ON college_placement_offers(application_id);
CREATE INDEX idx_student_offer ON college_placement_offers(student_id);
CREATE INDEX idx_offer_company ON college_placement_offers(company_id);
CREATE INDEX idx_offer_status ON college_placement_offers(status);
CREATE INDEX idx_joining ON college_placement_offers(joining_date);
CREATE INDEX idx_response ON college_placement_offers(student_response);

ALTER TABLE college_placement_offers
    ADD CONSTRAINT fk_offer_application FOREIGN KEY (application_id) REFERENCES college_placement_applications(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_offer_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_offer_company FOREIGN KEY (company_id) REFERENCES college_industry_partners(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_placement_officer FOREIGN KEY (placement_officer_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT uk_student_offer UNIQUE (student_id, company_id, joining_date);

-- -----------------------------------------------------------------------------
-- 6.14 COLLEGE_INDUSTRY_VISITS
-- -----------------------------------------------------------------------------
CREATE TABLE college_industry_visits (
    id BIGSERIAL PRIMARY KEY,
    visit_code VARCHAR(50) UNIQUE NOT NULL,
    company_id BIGINT NOT NULL,
    visit_title VARCHAR(500) NOT NULL,
    purpose VARCHAR(50) DEFAULT 'student_visit' CHECK (purpose IN ('faculty_training', 'student_visit', 'research_collaboration', 'moU_signing', 'other')),
    visit_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    location_address TEXT,
    contact_person_name VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    max_participants INT,
    participant_type VARCHAR(50) DEFAULT 'students' CHECK (participant_type IN ('students', 'faculty', 'both')),
    participant_departments JSONB,
    faculty_coordinator_id BIGINT NOT NULL,
    transportation_required BOOLEAN DEFAULT FALSE,
    transportation_details TEXT,
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    funding_source VARCHAR(50) DEFAULT 'department' CHECK (funding_source IN ('department', 'college', 'sponsor', 'self')),
    objectives TEXT,
    outcomes TEXT,
    report_url TEXT,
    photos_urls JSONB,
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'planned' CHECK (status IN ('planned', 'approved', 'scheduled', 'completed', 'cancelled')),
    cancellation_reason TEXT,
    feedback_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_visit_code ON college_industry_visits(visit_code);
CREATE INDEX idx_visit_company ON college_industry_visits(company_id);
CREATE INDEX idx_visit_dates ON college_industry_visits(visit_date);
CREATE INDEX idx_visit_status ON college_industry_visits(status);
CREATE INDEX idx_approval ON college_industry_visits(is_approved);
CREATE INDEX idx_coordinator ON college_industry_visits(faculty_coordinator_id);

ALTER TABLE college_industry_visits
    ADD CONSTRAINT fk_visit_company FOREIGN KEY (company_id) REFERENCES college_industry_partners(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_faculty_coordinator FOREIGN KEY (faculty_coordinator_id) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- ============================================================================
-- PLAN 6 COMPLETE: 14 tables created for PostgreSQL
-- ============================================================================
