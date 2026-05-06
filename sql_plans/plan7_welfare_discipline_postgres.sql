-- ============================================================================
-- PLAN 7: STUDENT WELFARE & DISCIPLINE (12 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 7.1 COLLEGE_COUNSELING_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE college_counseling_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category_type VARCHAR(50) DEFAULT 'personal' CHECK (category_type IN ('academic', 'personal', 'career', 'family', 'mental_health', 'social')),
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_counseling_slug ON college_counseling_categories(slug);
CREATE INDEX idx_counseling_type ON college_counseling_categories(category_type);
CREATE INDEX idx_counseling_active ON college_counseling_categories(is_active);

-- -----------------------------------------------------------------------------
-- 7.2 COLLEGE_STUDENT_COUNSELING
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_counseling (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    counselor_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    duration_minutes INT DEFAULT 60 CHECK (duration_minutes > 0),
    is_group_session BOOLEAN DEFAULT FALSE,
    group_session_id BIGINT,
    session_type VARCHAR(50) DEFAULT 'personal' CHECK (session_type IN ('academic', 'career', 'personal', 'family', 'crisis_intervention', 'follow_up')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    reason_for_visit TEXT NOT NULL,
    session_notes TEXT,
    recommendations TEXT,
    referrals_made JSONB,
    follow_up_required BOOLEAN DEFAULT FALSE,
    next_session_date DATE,
    confidentiality_level VARCHAR(50) DEFAULT 'standard' CHECK (confidentiality_level IN ('standard', 'sensitive', 'confidential')),
    emergency_contacted BOOLEAN DEFAULT FALSE,
    emergency_contact_time TIMESTAMP,
    crisis_flag BOOLEAN DEFAULT FALSE,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP,
    parent_response VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    closed_at TIMESTAMP,
    closed_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_counseling_student ON college_student_counseling(student_id);
CREATE INDEX idx_counselor ON college_student_counseling(counselor_id);
CREATE INDEX idx_category ON college_student_counseling(category_id);
CREATE INDEX idx_counseling_dates ON college_student_counseling(session_date, next_session_date);
CREATE INDEX idx_priority ON college_student_counseling(priority);
CREATE INDEX idx_crisis ON college_student_counseling(crisis_flag);
CREATE INDEX idx_followup ON college_student_counseling(follow_up_required, next_session_date);

ALTER TABLE college_student_counseling
    ADD CONSTRAINT fk_counseling_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_counseling_counselor FOREIGN KEY (counselor_id) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_counseling_category FOREIGN KEY (category_id) REFERENCES college_counseling_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_group_session FOREIGN KEY (group_session_id) REFERENCES college_student_counseling(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_closed_by FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.3 COLLEGE_STUDENT_WELFARE_PROGRAMS
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_welfare_programs (
    id BIGSERIAL PRIMARY KEY,
    program_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    program_type VARCHAR(50) DEFAULT 'financial_aid' CHECK (program_type IN ('financial_aid', 'scholarship', 'remedial', 'enrichment', 'health', 'mental_health', 'special_needs', 'career_guidance', 'other')),
    department_id BIGINT,
    eligibility_criteria JSONB,
    benefits_description TEXT,
    monetary_benefit DECIMAL(10,2) DEFAULT 0.00,
    benefit_frequency VARCHAR(50) DEFAULT 'one_time' CHECK (benefit_frequency IN ('one_time', 'monthly', 'quarterly', 'semester', 'annually')),
    total_slots INT,
    current_enrolled INT DEFAULT 0,
    application_start_date DATE,
    application_end_date DATE,
    review_process JSONB,
    required_documents JSONB,
    is_need_based BOOLEAN DEFAULT FALSE,
    is_merit_based BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_automated_enrollment BOOLEAN DEFAULT FALSE,
    coordinator_id BIGINT NOT NULL,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_program_code ON college_student_welfare_programs(program_code);
CREATE INDEX idx_program_type_active ON college_student_welfare_programs(program_type, is_active);
CREATE INDEX idx_welfare_department ON college_student_welfare_programs(department_id);
CREATE INDEX idx_welfare_dates ON college_student_welfare_programs(application_start_date, application_end_date);
CREATE INDEX idx_coordinator ON college_student_welfare_programs(coordinator_id);

ALTER TABLE college_student_welfare_programs
    ADD CONSTRAINT fk_welfare_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_coordinator FOREIGN KEY (coordinator_id) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_enrollment_limit CHECK (current_enrolled <= total_slots),
    ADD CONSTRAINT chk_dates_valid CHECK (application_end_date IS NULL OR application_end_date >= application_start_date);

-- -----------------------------------------------------------------------------
-- 7.4 COLLEGE_STUDENT_WELFARE_ENROLLMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_welfare_enrollments (
    id BIGSERIAL PRIMARY KEY,
    program_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    enrollment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'suspended', 'terminated', 'expired')),
    benefit_amount DECIMAL(10,2),
    benefit_frequency VARCHAR(50),
    next_disbursement_date DATE,
    last_disbursement_date DATE,
    disbursements_made INT DEFAULT 0,
    total_disbursed DECIMAL(12,2) DEFAULT 0.00,
    renewal_eligible BOOLEAN DEFAULT FALSE,
    renewal_application_id BIGINT,
    exit_reason TEXT,
    exit_date DATE,
    case_worker_id BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_program_student_active ON college_student_welfare_enrollments(program_id, student_id, status) WHERE status = 'active';
CREATE INDEX idx_welfare_program ON college_student_welfare_enrollments(program_id);
CREATE INDEX idx_welfare_student ON college_student_welfare_enrollments(student_id);
CREATE INDEX idx_welfare_status ON college_student_welfare_enrollments(status);
CREATE INDEX idx_renewal ON college_student_welfare_enrollments(renewal_eligible, next_disbursement_date);

ALTER TABLE college_student_welfare_enrollments
    ADD CONSTRAINT fk_enrollment_program FOREIGN KEY (program_id) REFERENCES college_student_welfare_programs(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_enrollment_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_renewal_application FOREIGN KEY (renewal_application_id) REFERENCES college_student_welfare_enrollments(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_case_worker FOREIGN KEY (case_worker_id) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.5 COLLEGE_STUDENT_LEAVE_APPLICATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_leave_applications (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    leave_type VARCHAR(50) NOT NULL CHECK (leave_type IN ('medical', 'personal', 'family', 'academic', 'sports', 'placement', 'other')),
    reason TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INT GENERATED ALWAYS AS ((end_date - start_date) + 1) STORED,
    supporting_document_url TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relation VARCHAR(50),
    address_during_leave TEXT,
    alternative_contact VARCHAR(20),
    is_hostel_resident BOOLEAN DEFAULT FALSE,
    hostel_room_number VARCHAR(50),
    leaving_from_hostel BOOLEAN DEFAULT FALSE,
    expected_return_date DATE,
    actual_return_date DATE,
    status VARCHAR(50) DEFAULT 'submitted' CHECK (status IN ('draft', 'submitted', 'pending_approval', 'approved', 'rejected', 'cancelled', 'completed')),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    approval_remarks TEXT,
    rejected_by BIGINT,
    rejected_at TIMESTAMP,
    rejection_reason TEXT,
    extension_requested BOOLEAN DEFAULT FALSE,
    extension_granted BOOLEAN DEFAULT FALSE,
    extension_new_end_date DATE,
    conflict_with_exam BOOLEAN DEFAULT FALSE,
    conflict_details TEXT,
    attendance_impact_calculated BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leave_student_status ON college_student_leave_applications(student_id, status);
CREATE INDEX idx_leave_dates ON college_student_leave_applications(start_date, end_date);
CREATE INDEX idx_leave_type ON college_student_leave_applications(leave_type);
CREATE INDEX idx_approval ON college_student_leave_applications(approved_by, approved_at);
CREATE INDEX idx_submitted ON college_student_leave_applications(submitted_at);

ALTER TABLE college_student_leave_applications
    ADD CONSTRAINT fk_leave_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_rejected_by FOREIGN KEY (rejected_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_end_after_start CHECK (end_date >= start_date),
    ADD CONSTRAINT chk_actual_return CHECK (actual_return_date IS NULL OR actual_return_date >= start_date);

-- -----------------------------------------------------------------------------
-- 7.6 COLLEGE_STUDENT_WARNINGS
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_warnings (
    id BIGSERIAL PRIMARY KEY,
    warning_number VARCHAR(50) UNIQUE NOT NULL,
    student_id BIGINT NOT NULL,
    warning_type VARCHAR(50) DEFAULT 'academic' CHECK (warning_type IN ('academic', 'attendance', 'disciplinary', 'behavioral', 'financial', 'multiple')),
    severity VARCHAR(20) DEFAULT 'moderate' CHECK (severity IN ('minor', 'moderate', 'major', 'critical')),
    issuing_authority VARCHAR(50) DEFAULT 'hod' CHECK (issuing_authority IN ('hod', 'principal', 'dean', 'disciplinary_committee', 'warden')),
    issued_by BIGINT NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    related_students JSONB,
    related_incident_id BIGINT,
    supporting_evidence JSONB,
    previous_warnings_count INT DEFAULT 0,
    previous_warning_ids JSONB,
    expected_corrective_action TEXT,
    deadline_for_compliance DATE,
    compliance_status VARCHAR(50) DEFAULT 'pending' CHECK (compliance_status IN ('pending', 'in_progress', 'complied', 'violated', 'exempted')),
    compliance_notes TEXT,
    compliance_verified_by BIGINT,
    compliance_verified_at TIMESTAMP,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP,
    parent_acknowledged BOOLEAN DEFAULT FALSE,
    parent_acknowledged_at TIMESTAMP,
    appeal_filed BOOLEAN DEFAULT FALSE,
    appeal_details TEXT,
    appeal_decided BOOLEAN DEFAULT FALSE,
    appeal_outcome TEXT,
    appeal_decided_by BIGINT,
    appeal_decided_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    superseded_by_warning_id BIGINT,
    archived_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_warning_number ON college_student_warnings(warning_number);
CREATE INDEX idx_warning_student_type ON college_student_warnings(student_id, warning_type);
CREATE INDEX idx_severity ON college_student_warnings(severity);
CREATE INDEX idx_issuer ON college_student_warnings(issued_by);
CREATE INDEX idx_deadline ON college_student_warnings(deadline_for_compliance);
CREATE INDEX idx_compliance ON college_student_warnings(compliance_status);
CREATE INDEX idx_issued ON college_student_warnings(issued_at);

ALTER TABLE college_student_warnings
    ADD CONSTRAINT fk_warning_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issued_by FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_compliance_verified_by FOREIGN KEY (compliance_verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_appeal_decided_by FOREIGN KEY (appeal_decided_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_superseded FOREIGN KEY (superseded_by_warning_id) REFERENCES college_student_warnings(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_deadline CHECK (deadline_for_compliance IS NULL OR deadline_for_compliance >= DATE(issued_at));

-- -----------------------------------------------------------------------------
-- 7.7 SCHOOL_DISCIPLINARY_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_disciplinary_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    severity_level VARCHAR(20) DEFAULT 'moderate' CHECK (severity_level IN ('minor', 'moderate', 'major', 'critical')),
    points INT DEFAULT 0,
    recommended_action TEXT,
    is_reportable BOOLEAN DEFAULT FALSE,
    category_group VARCHAR(50) DEFAULT 'behavioral' CHECK (category_group IN ('academic', 'behavioral', 'safety', 'property', 'harassment', 'substance', 'technology', 'other')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_disc_category_code ON school_disciplinary_categories(code);
CREATE INDEX idx_severity ON school_disciplinary_categories(severity_level);
CREATE INDEX idx_category_group ON school_disciplinary_categories(category_group);

-- -----------------------------------------------------------------------------
-- 7.8 SCHOOL_DISCIPLINARY_ACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_disciplinary_actions (
    id BIGSERIAL PRIMARY KEY,
    incident_number VARCHAR(50) UNIQUE NOT NULL,
    student_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    reported_by BIGINT NOT NULL,
    incident_date DATE NOT NULL,
    incident_time TIME,
    location VARCHAR(255),
    detailed_description TEXT NOT NULL,
    witnesses JSONB,
    evidence_urls JSONB,
    immediate_action_taken TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    investigation_status VARCHAR(50) DEFAULT 'pending' CHECK (investigation_status IN ('pending', 'in_progress', 'student_interviewed', 'witnesses_interviewed', 'evidence_reviewed', 'recommendation_ready', 'hearing_scheduled', 'closed')),
    investigator_id BIGINT,
    investigation_notes TEXT,
    investigation_completed_at TIMESTAMP,
    hearing_scheduled_date DATE,
    hearing_time TIME,
    hearing_venue VARCHAR(255),
    hearing_panel JSONB,
    hearing_conducted BOOLEAN DEFAULT FALSE,
    hearing_notes TEXT,
    hearing_recording_url TEXT,
    finding_guilty BOOLEAN,
    finding_notes TEXT,
    recommended_penalty TEXT,
    final_decision TEXT,
    final_penalty JSONB,
    penalty_effective_from DATE,
    penalty_duration_days INT,
    penalty_expiry_date DATE,
    penalty_issuing_authority BIGINT,
    penalty_issued_at TIMESTAMP,
    appeal_available BOOLEAN DEFAULT TRUE,
    appeal_deadline_date DATE,
    appeal_submitted BOOLEAN DEFAULT FALSE,
    appeal_details TEXT,
    appeal_decision TEXT,
    appeal_decided_by BIGINT,
    appeal_decided_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'under_investigation', 'hearing_pending', 'penalty_imposed', 'appeal_pending', 'closed', 'expunged')),
    resolution_notes TEXT,
    closed_by BIGINT,
    closed_at TIMESTAMP,
    case_sensitivity VARCHAR(50) DEFAULT 'confidential' CHECK (case_sensitivity IN ('public', 'confidential', 'restricted')),
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP,
    parent_meeting_scheduled BOOLEAN DEFAULT FALSE,
    parent_meeting_datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_incident_number ON school_disciplinary_actions(incident_number);
CREATE INDEX idx_disc_student ON school_disciplinary_actions(student_id);
CREATE INDEX idx_category ON school_disciplinary_actions(category_id);
CREATE INDEX idx_reporter ON school_disciplinary_actions(reported_by);
CREATE INDEX idx_disc_dates ON school_disciplinary_actions(incident_date, hearing_scheduled_date);
CREATE INDEX idx_status ON school_disciplinary_actions(status);
CREATE INDEX idx_investigator ON school_disciplinary_actions(investigator_id);
CREATE INDEX idx_hearing ON school_disciplinary_actions(hearing_scheduled_date, hearing_conducted);

ALTER TABLE school_disciplinary_actions
    ADD CONSTRAINT fk_action_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_action_category FOREIGN KEY (category_id) REFERENCES school_disciplinary_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_reported_by FOREIGN KEY (reported_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_investigator FOREIGN KEY (investigator_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_penalty_issuing_authority FOREIGN KEY (penalty_issuing_authority) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_appeal_decided_by FOREIGN KEY (appeal_decided_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_closed_by FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.9 SCHOOL_DISCIPLINARY_HEARINGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_disciplinary_hearings (
    id BIGSERIAL PRIMARY KEY,
    disciplinary_action_id BIGINT UNIQUE NOT NULL,
    hearing_date DATE NOT NULL,
    hearing_time TIME NOT NULL,
    venue VARCHAR(255),
    panel_members JSONB,
    student_present BOOLEAN DEFAULT FALSE,
    student_representative_present BOOLEAN DEFAULT FALSE,
    parent_guardian_present BOOLEAN DEFAULT FALSE,
    parent_guardian_name VARCHAR(255),
    student_statement TEXT,
    evidence_presented JSONB,
    witness_testimonies JSONB,
    panel_deliberation_notes TEXT,
    verbal_warning_given BOOLEAN DEFAULT FALSE,
    written_warning_issued BOOLEAN DEFAULT FALSE,
    suspension_imposed BOOLEAN DEFAULT FALSE,
    suspension_start_date DATE,
    suspension_end_date DATE,
    community_service_assigned BOOLEAN DEFAULT FALSE,
    community_service_hours INT,
    restitution_amount DECIMAL(10,2),
    probation_imposed BOOLEAN DEFAULT FALSE,
    probation_end_date DATE,
    expulsion_recommended BOOLEAN DEFAULT FALSE,
    other_penalties JSONB,
    decision_summary TEXT,
    decision_rationale TEXT,
    decision_recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decision_recorded_by BIGINT NOT NULL,
    transcript_prepared BOOLEAN DEFAULT FALSE,
    transcript_url TEXT,
    followup_required BOOLEAN DEFAULT FALSE,
    followup_date DATE,
    followup_assigned_to BIGINT,
    appeal_rights_explained BOOLEAN DEFAULT FALSE,
    appeal_rights_explained_by BIGINT,
    appeal_deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hearing_disciplinary ON school_disciplinary_hearings(disciplinary_action_id);
CREATE INDEX idx_hearing_dates ON school_disciplinary_hearings(hearing_date, followup_date);
CREATE INDEX idx_panel ON school_disciplinary_hearings(decision_recorded_by);
CREATE INDEX idx_appeal_deadline ON school_disciplinary_hearings(appeal_deadline, appeal_rights_explained);

ALTER TABLE school_disciplinary_hearings
    ADD CONSTRAINT fk_hearing_action FOREIGN KEY (disciplinary_action_id) REFERENCES school_disciplinary_actions(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_decision_recorded_by FOREIGN KEY (decision_recorded_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_followup_assigned FOREIGN KEY (followup_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.10 SCHOOL_STUDENT_HEALTH_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_health_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT UNIQUE NOT NULL,
    blood_group VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    height_cm DECIMAL(5,2) CHECK (height_cm > 0),
    weight_kg DECIMAL(5,2) CHECK (weight_kg > 0),
    bmi DECIMAL(4,2) GENERATED ALWAYS AS (weight_kg / POWER(height_cm/100, 2)) STORED CHECK (bmi BETWEEN 10 AND 50),
    known_allergies JSONB,
    chronic_illnesses JSONB,
    medications JSONB,
    regular_medications TEXT,
    emergency_medications TEXT,
    immunizations JSONB,
    last_physical_exam_date DATE,
    last_dental_checkup DATE,
    last_eye_checkup DATE,
    hearing_status VARCHAR(50) DEFAULT 'normal' CHECK (hearing_status IN ('normal', 'impaired', 'deaf')),
    vision_status VARCHAR(50) DEFAULT 'normal' CHECK (vision_status IN ('normal', 'corrected', 'impaired', 'blind')),
    physical_limitations TEXT,
    dietary_restrictions JSONB,
    mental_health_conditions JSONB,
    mental_health_notes TEXT,
    surgeon_general_clearance BOOLEAN DEFAULT FALSE,
    sports_clearance BOOLEAN DEFAULT FALSE,
    sports_clearance_valid_until DATE,
    doctor_name VARCHAR(255),
    doctor_phone VARCHAR(20),
    doctor_address TEXT,
    insurance_provider VARCHAR(255),
    insurance_policy_number VARCHAR(100),
    insurance_group_number VARCHAR(50),
    insurance_contact_phone VARCHAR(20),
    emergency_contact_1_name VARCHAR(255),
    emergency_contact_1_relation VARCHAR(50),
    emergency_contact_1_phone VARCHAR(20),
    emergency_contact_2_name VARCHAR(255),
    emergency_contact_2_relation VARCHAR(50),
    emergency_contact_2_phone VARCHAR(20),
    primary_care_physician VARCHAR(255),
    last_updated_by BIGINT,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consent_for_treatment BOOLEAN DEFAULT FALSE,
    consent_for_emergency_care BOOLEAN DEFAULT FALSE,
    consent_for_sharing_info BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_student ON school_student_health_records(student_id);
CREATE INDEX idx_blood ON school_student_health_records(blood_group);
CREATE GIN INDEX idx_health_allergies ON school_student_health_records USING GIN (known_allergies);
CREATE GIN INDEX idx_chronic ON school_student_health_records USING GIN (chronic_illnesses);
CREATE INDEX idx_sports_clearance ON school_student_health_records(sports_clearance, sports_clearance_valid_until);
CREATE INDEX idx_insurance ON school_student_health_records(insurance_provider, insurance_policy_number);

ALTER TABLE school_student_health_records
    ADD CONSTRAINT fk_health_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_last_updated_by FOREIGN KEY (last_updated_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.11 SCHOOL_VACCINATION_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vaccination_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    vaccine_name VARCHAR(255) NOT NULL,
    vaccine_type VARCHAR(100),
    dose_number INT DEFAULT 1 CHECK (dose_number >= 1),
    total_doses_required INT NOT NULL CHECK (total_doses_required >= dose_number),
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    administered_by VARCHAR(255) NOT NULL,
    administered_by_title VARCHAR(100),
    facility_name VARCHAR(255),
    facility_address TEXT,
    certificate_url TEXT,
    lot_number VARCHAR(100),
    manufacturer VARCHAR(255),
    is_mandatory BOOLEAN DEFAULT FALSE,
    exemption_reason TEXT,
    exemption_granted_by BIGINT,
    exemption_granted_at TIMESTAMP,
    verified_by BIGINT,
    verified_at TIMESTAMP,
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_vaccine_dose ON school_vaccination_records(student_id, vaccine_name, dose_number);
CREATE INDEX idx_vacc_student ON school_vaccination_records(student_id);
CREATE INDEX idx_vaccine ON school_vaccination_records(vaccine_name);
CREATE INDEX idx_vacc_dates ON school_vaccination_records(vaccination_date, next_due_date);
CREATE INDEX idx_mandatory ON school_vaccination_records(is_mandatory);
CREATE INDEX idx_verified ON school_vaccination_records(verified_by, verified_at);

ALTER TABLE school_vaccination_records
    ADD CONSTRAINT fk_vacc_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exemption_by FOREIGN KEY (exemption_granted_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.12 SCHOOL_MEDICAL_VISITS
-- -----------------------------------------------------------------------------
CREATE TABLE school_medical_visits (
    id BIGSERIAL PRIMARY KEY,
    visit_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    student_id BIGINT NOT NULL,
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    visit_type VARCHAR(50) DEFAULT 'illness' CHECK (visit_type IN ('injury', 'illness', 'routine_checkup', 'medication', 'vaccination', 'mental_health', 'other')),
    presenting_complaint TEXT NOT NULL,
    symptoms_observed TEXT,
    vitals JSONB,
    treatment_provided TEXT,
    medications_given JSONB,
    bandage_applied BOOLEAN DEFAULT FALSE,
    injury_location VARCHAR(100),
    injury_severity VARCHAR(20) DEFAULT 'minor' CHECK (injury_severity IN ('minor', 'moderate', 'severe')),
    referred_to_hospital BOOLEAN DEFAULT FALSE,
    hospital_name VARCHAR(255),
    referral_reason TEXT,
    parent_contacted BOOLEAN DEFAULT FALSE,
    parent_contacted_at TIMESTAMP,
    parent_contact_method VARCHAR(50),
    parent_response VARCHAR(50),
    student_sent_home BOOLEAN DEFAULT FALSE,
    sent_home_reason TEXT,
    ambulance_called BOOLEAN DEFAULT FALSE,
    ambulance_service VARCHAR(255),
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    follow_up_notes TEXT,
    treated_by BIGINT NOT NULL,
    case_notes TEXT,
    is_confidential BOOLEAN DEFAULT FALSE,
    confidentiality_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_visit_id ON school_medical_visits(visit_id);
CREATE INDEX idx_medical_student_date ON school_medical_visits(student_id, visit_date);
CREATE INDEX idx_visit_type ON school_medical_visits(visit_type);
CREATE INDEX idx_followup ON school_medical_visits(follow_up_required, follow_up_date);
CREATE INDEX idx_treated_by ON school_medical_visits(treated_by);
CREATE INDEX idx_created ON school_medical_visits(created_at);

ALTER TABLE school_medical_visits
    ADD CONSTRAINT fk_medical_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_treated_by FOREIGN KEY (treated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 7.13 COLLEGE_STUDENT_SPECIAL_NEEDS
-- -----------------------------------------------------------------------------
CREATE TABLE college_student_special_needs (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT UNIQUE NOT NULL,
    disability_type VARCHAR(50) NOT NULL CHECK (disability_type IN ('physical', 'visual', 'hearing', 'learning', 'mental_health', 'chronic_illness', 'multiple')),
    disability_certificate_url TEXT,
    diagnosis_details TEXT,
    functional_limitations TEXT,
    required_accommodations JSONB,
    current_accommodations JSONB,
    recommended_by VARCHAR(255),
    recommendation_date DATE,
    reviewed_by BIGINT,
    reviewed_date DATE,
    review_frequency_months INT DEFAULT 12,
    next_review_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_special_needs_student ON college_student_special_needs(student_id);
CREATE INDEX idx_disability_type ON college_student_special_needs(disability_type);
CREATE INDEX idx_active ON college_student_special_needs(is_active);
CREATE INDEX idx_next_review ON college_student_special_needs(next_review_date);

ALTER TABLE college_student_special_needs
    ADD CONSTRAINT fk_special_needs_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_reviewed_by FOREIGN KEY (reviewed_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.14 SCHOOL_STUDENT_SAFETY_INCIDENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_safety_incidents (
    id BIGSERIAL PRIMARY KEY,
    incident_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    incident_type VARCHAR(50) DEFAULT 'accident' CHECK (incident_type IN ('accident', 'near_miss', 'hazard', 'injury', 'property_damage', 'intentional_harm')),
    reported_by BIGINT NOT NULL,
    incident_date DATE NOT NULL,
    incident_time TIME,
    location_type VARCHAR(50) DEFAULT 'classroom' CHECK (location_type IN ('classroom', 'corridor', 'playground', 'lab', 'canteen', 'toilet', 'bus', 'off_campus')),
    specific_location VARCHAR(255),
    students_involved JSONB,
    staff_witnesses JSONB,
    description TEXT NOT NULL,
    root_cause_analysis TEXT,
    immediate_actions_taken TEXT,
    injuries_sustained BOOLEAN DEFAULT FALSE,
    injury_details JSONB,
    medical_attention_required BOOLEAN DEFAULT FALSE,
    hospital_transport BOOLEAN DEFAULT FALSE,
    property_damage BOOLEAN DEFAULT FALSE,
    property_damage_value DECIMAL(12,2),
    police_involved BOOLEAN DEFAULT FALSE,
    police_report_filed BOOLEAN DEFAULT FALSE,
    police_report_number VARCHAR(100),
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP,
    parent_contact_details JSONB,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_assigned_to BIGINT,
    follow_up_due_date DATE,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),
    closed_at TIMESTAMP,
    closed_by BIGINT,
    preventive_measures TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_incident_id ON school_student_safety_incidents(incident_id);
CREATE INDEX idx_safety_dates ON school_student_safety_incidents(incident_date, follow_up_due_date);
CREATE INDEX idx_safety_reporter ON school_student_safety_incidents(reported_by);
CREATE INDEX idx_safety_status ON school_student_safety_incidents(status);
CREATE INDEX idx_incident_type ON school_student_safety_incidents(incident_type);
CREATE INDEX idx_location ON school_student_safety_incidents(location_type, specific_location(255));
CREATE INDEX idx_followup ON school_student_safety_incidents(follow_up_required, follow_up_assigned_to);

ALTER TABLE school_student_safety_incidents
    ADD CONSTRAINT fk_safety_reported_by FOREIGN KEY (reported_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_followup_assigned FOREIGN KEY (follow_up_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_closed_by FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- ============================================================================
-- PLAN 7 COMPLETE: 12 tables created for PostgreSQL
-- ============================================================================
