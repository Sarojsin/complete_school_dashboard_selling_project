-- ============================================================================
-- PLAN 7: STUDENT WELFARE & DISCIPLINE (12 tables)
-- ============================================================================
-- Counseling, disciplinary tracking, leave management, health records
-- Dependencies: college_students, college_teachers, college_parents
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 7.1 COLLEGE_COUNSELING_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_counseling_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category_type ENUM('academic', 'personal', 'career', 'family', 'mental_health', 'social') DEFAULT 'personal',
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_type (category_type),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Counseling session type taxonomy';

-- -----------------------------------------------------------------------------
-- 7.2 COLLEGE_STUDENT_COUNSELING
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_counseling (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    counselor_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    duration_minutes INT UNSIGNED DEFAULT 60,
    is_group_session BOOLEAN DEFAULT FALSE,
    group_session_id BIGINT UNSIGNED,
    session_type ENUM('academic', 'career', 'personal', 'family', 'crisis_intervention', 'follow_up') DEFAULT 'personal',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    reason_for_visit TEXT NOT NULL,
    session_notes LONGTEXT,
    recommendations TEXT,
    referrals_made JSON, -- ["psychologist", "specialist", "external_agency"]
    follow_up_required BOOLEAN DEFAULT FALSE,
    next_session_date DATE,
    confidentiality_level ENUM('standard', 'sensitive', 'confidential') DEFAULT 'standard',
    emergency_contacted BOOLEAN DEFAULT FALSE,
    emergency_contact_time TIMESTAMP NULL,
    crisis_flag BOOLEAN DEFAULT FALSE,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP NULL,
    parent_response ENUM('acknowledged', 'discussed', 'concerned', 'no_response'),
    is_active BOOLEAN DEFAULT TRUE, -- for ongoing therapy
    closed_at TIMESTAMP NULL,
    closed_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_student (student_id),
    INDEX idx_counselor (counselor_id),
    INDEX idx_category (category_id),
    INDEX idx_dates (session_date, next_session_date),
    INDEX idx_priority (priority),
    INDEX idx_crisis (crisis_flag),
    INDEX idx_followup (follow_up_required, next_session_date),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES college_counseling_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (group_session_id) REFERENCES college_student_counseling(id) ON DELETE SET NULL,
    FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (duration_minutes > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student counseling session records';

-- -----------------------------------------------------------------------------
-- 7.3 COLLEGE_STUDENT_WELFARE_PROGRAMS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_welfare_programs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    program_type ENUM('financial_aid', 'scholarship', 'remedial', 'enrichment', 'health', 'mental_health', 'special_needs', 'career_guidance', 'other') DEFAULT 'financial_aid',
    department_id BIGINT UNSIGNED,
    eligibility_criteria JSON, -- {"min_cgpa": 7.5, "income_threshold": 500000}
    benefits_description TEXT,
    monetary_benefit DECIMAL(10,2) DEFAULT 0.00,
    benefit_frequency ENUM('one_time', 'monthly', 'quarterly', 'semester', 'annually') DEFAULT 'one_time',
    total_slots INT UNSIGNED,
    current_enrolled INT UNSIGNED DEFAULT 0,
    application_start_date DATE,
    application_end_date DATE,
    review_process JSON, -- stages
    required_documents JSON, -- ["income_certificate", "marksheet"]
    is_need_based BOOLEAN DEFAULT FALSE,
    is_merit_based BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_automated_enrollment BOOLEAN DEFAULT FALSE, -- auto-qualify based on criteria
    coordinator_id BIGINT UNSIGNED NOT NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_program_code (program_code),
    INDEX idx_type_active (program_type, is_active),
    INDEX idx_department (department_id),
    INDEX idx_dates (application_start_date, application_end_date),
    INDEX idx_coordinator (coordinator_id),
    FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE SET NULL,
    FOREIGN KEY (coordinator_id) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    CHECK (current_enrolled <= total_slots),
    CHECK (application_end_date >= application_start_date OR application_end_date IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student welfare and support programs';

-- -----------------------------------------------------------------------------
-- 7.4 COLLEGE_STUDENT_WELFARE_ENROLLMENTS (Junction)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_welfare_enrollments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'completed', 'suspended', 'terminated', 'expired') DEFAULT 'active',
    benefit_amount DECIMAL(10,2), -- actual amount awarded
    benefit_frequency ENUM('one_time', 'monthly', 'quarterly', 'semester', 'annually'),
    next_disbursement_date DATE,
    last_disbursement_date DATE,
    disbursements_made INT UNSIGNED DEFAULT 0,
    total_disbursed DECIMAL(12,2) DEFAULT 0.00,
    renewal_eligible BOOLEAN DEFAULT FALSE,
    renewal_application_id BIGINT UNSIGNED,
    exit_reason TEXT,
    exit_date DATE,
    case_worker_id BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_program_student_active (program_id, student_id, status),
    INDEX idx_program (program_id),
    INDEX idx_student (student_id),
    INDEX idx_status (status),
    INDEX idx_renewal (renewal_eligible, next_disbursement_date),
    FOREIGN KEY (program_id) REFERENCES college_student_welfare_programs(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (renewal_application_id) REFERENCES college_student_welfare_enrollments(id) ON DELETE SET NULL,
    FOREIGN KEY (case_worker_id) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student enrollment in welfare programs';

-- -----------------------------------------------------------------------------
-- 7.5 COLLEGE_STUDENT_LEAVE_APPLICATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_leave_applications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    leave_type ENUM('medical', 'personal', 'family', 'academic', 'sports', 'placement', 'other') NOT NULL,
    reason TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INT GENERATED ALWAYS AS (DATEDIFF(end_date, start_date) + 1) STORED,
    supporting_document_url TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relation VARCHAR(50),
    address_during_leave TEXT,
    alternative_contact VARCHAR(20),
    is_ hostel_resident BOOLEAN DEFAULT FALSE,
    hostel_room_number VARCHAR(50),
    leaving_from_hostel BOOLEAN DEFAULT FALSE,
    expected_return_date DATE,
    actual_return_date DATE,
    status ENUM('draft', 'submitted', 'pending_approval', 'approved', 'rejected', 'cancelled', 'completed') DEFAULT 'submitted',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP NULL,
    approval_remarks TEXT,
    rejected_by BIGINT UNSIGNED,
    rejected_at TIMESTAMP NULL,
    rejection_reason TEXT,
    extension_requested BOOLEAN DEFAULT FALSE,
    extension_granted BOOLEAN DEFAULT FALSE,
    extension_new_end_date DATE,
    conflict_with_exam BOOLEAN DEFAULT FALSE,
    conflict_details TEXT,
    attendance_impact_calculated BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_student_status (student_id, status),
    INDEX idx_dates (start_date, end_date),
    INDEX idx_leave_type (leave_type),
    INDEX idx_approval (approved_by, approved_at),
    INDEX idx_submitted (submitted_at),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (rejected_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (end_date >= start_date),
    CHECK (actual_return_date IS NULL OR actual_return_date >= start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student leave requests and approvals';

-- -----------------------------------------------------------------------------
-- 7.6 COLLEGE_STUDENT_WARNINGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_warnings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    warning_number VARCHAR(50) UNIQUE NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    warning_type ENUM('academic', 'attendance', 'disciplinary', 'behavioral', 'financial', 'multiple') DEFAULT 'academic',
    severity ENUM('minor', 'moderate', 'major', 'critical') DEFAULT 'moderate',
    issuing_authority ENUM('hod', 'principal', 'dean', 'disciplinary_committee', 'warden') DEFAULT 'hod',
    issued_by BIGINT UNSIGNED NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL,
    description LONGTEXT NOT NULL,
    related_students JSON, -- co-accused or involved
    related_incident_id BIGINT UNSIGNED, -- link to disciplinary_actions
    supporting_evidence JSON, -- ["screenshot1.jpg", "witness_statement.pdf"]
    previous_warnings_count INT UNSIGNED DEFAULT 0,
    previous_warning_ids JSON,
    expected_corrective_action TEXT,
    deadline_for_compliance DATE,
    compliance_status ENUM('pending', 'in_progress', 'complied', 'violated', 'exempted') DEFAULT 'pending',
    compliance_notes TEXT,
    compliance_verified_by BIGINT UNSIGNED,
    compliance_verified_at TIMESTAMP NULL,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP NULL,
    parent_acknowledged BOOLEAN DEFAULT FALSE,
    parent_acknowledged_at TIMESTAMP NULL,
    appeal_filed BOOLEAN DEFAULT FALSE,
    appeal_details TEXT,
    appeal_decided BOOLEAN DEFAULT FALSE,
    appeal_outcome TEXT,
    appeal_decided_by BIGINT UNSIGNED,
    appeal_decided_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    superseded_by_warning_id BIGINT UNSIGNED,
    archived_at TIMESTAMP NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_warning_number (warning_number),
    INDEX idx_student_type (student_id, warning_type),
    INDEX idx_severity (severity),
    INDEX idx_issuer (issued_by),
    INDEX idx_deadline (deadline_for_compliance),
    INDEX idx_compliance (compliance_status),
    INDEX idx_issued (issued_at),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (compliance_verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (appeal_decided_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (superseded_by_warning_id) REFERENCES college_student_warnings(id) ON DELETE SET NULL,
    CHECK (deadline_for_compliance IS NULL OR deadline_for_compliance >= DATE(issued_at))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Academic and behavioral warning system';

-- -----------------------------------------------------------------------------
-- 7.7 SCHOOL_DISCIPLINARY_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_disciplinary_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    severity_level ENUM('minor', 'moderate', 'major', 'critical') DEFAULT 'moderate',
    points INT DEFAULT 0, -- demerit points
    recommended_action TEXT, -- suggested penalties
    is_reportable BOOLEAN DEFAULT FALSE, -- appears on transcript?
    category_group ENUM('academic', 'behavioral', 'safety', 'property', 'harassment', 'substance', 'technology', 'other') DEFAULT 'behavioral',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_severity (severity_level),
    INDEX idx_group (category_group)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Disciplinary violation type taxonomy';

-- -----------------------------------------------------------------------------
-- 7.8 SCHOOL_DISCIPLINARY_ACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_disciplinary_actions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    incident_number VARCHAR(50) UNIQUE NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    reported_by BIGINT UNSIGNED NOT NULL, -- teacher/staff
    incident_date DATE NOT NULL,
    incident_time TIME,
    location VARCHAR(255),
    detailed_description LONGTEXT NOT NULL,
    witnesses JSON, -- student IDs or staff IDs
    evidence_urls JSON, -- photos, videos, documents
    immediate_action_taken TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    investigation_status ENUM('pending', 'in_progress', 'student_interviewed', 'witnesses_interviewed', 'evidence_reviewed', 'recommendation_ready', 'hearing_scheduled', 'closed') DEFAULT 'pending',
    investigator_id BIGINT UNSIGNED,
    investigation_notes LONGTEXT,
    investigation_completed_at TIMESTAMP NULL,
    hearing_scheduled_date DATE,
    hearing_time TIME,
    hearing_venue VARCHAR(255),
    hearing_panel JSON, -- [teacher_id1, teacher_id2, student_rep_id]
    hearing_conducted BOOLEAN DEFAULT FALSE,
    hearing_notes LONGTEXT,
    hearing_recording_url TEXT,
    finding_guilty BOOLEAN,
    finding_notes TEXT,
    recommended_penalty TEXT,
    final_decision TEXT,
    final_penalty JSON, -- structured penalty details
    penalty_effective_from DATE,
    penalty_duration_days INT,
    penalty_expiry_date DATE,
    penalty_issuing_authority BIGINT UNSIGNED,
    penalty_issued_at TIMESTAMP NULL,
    appeal_available BOOLEAN DEFAULT TRUE,
    appeal_deadline_date DATE,
    appeal_submitted BOOLEAN DEFAULT FALSE,
    appeal_details TEXT,
    appeal_decision TEXT,
    appeal_decided_by BIGINT UNSIGNED,
    appeal_decided_at TIMESTAMP NULL,
    status ENUM('open', 'under_investigation', 'hearing_pending', 'penalty_imposed', 'appeal_pending', 'closed', 'expunged') DEFAULT 'open',
    resolution_notes TEXT,
    closed_by BIGINT UNSIGNED,
    closed_at TIMESTAMP NULL,
    case_sensitivity ENUM('public', 'confidential', 'restricted') DEFAULT 'confidential',
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP NULL,
    parent_meeting_scheduled BOOLEAN DEFAULT FALSE,
    parent_meeting_datetime DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_incident_number (incident_number),
    INDEX idx_student (student_id),
    INDEX idx_category (category_id),
    INDEX idx_reporter (reported_by),
    INDEX idx_dates (incident_date, hearing_scheduled_date),
    INDEX idx_status (status),
    INDEX idx_severity (category_id), -- via category severity
    INDEX idx_investigator (investigator_id),
    INDEX idx_hearing (hearing_scheduled_date, hearing_conducted),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES school_disciplinary_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (reported_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (investigator_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (penalty_issuing_authority) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (appeal_decided_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student disciplinary incidents and proceedings';

-- -----------------------------------------------------------------------------
-- 7.9 SCHOOL_DISCIPLINARY_HEARINGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_disciplinary_hearings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    disciplinary_action_id BIGINT UNIQUE NOT NULL, -- one hearing per case (extendable)
    hearing_date DATE NOT NULL,
    hearing_time TIME NOT NULL,
    venue VARCHAR(255),
    panel_members JSON, -- [{teacher_id, role, vote_weight}]
    student_present BOOLEAN DEFAULT FALSE,
    student_representative_present BOOLEAN DEFAULT FALSE,
    parent_guardian_present BOOLEAN DEFAULT FALSE,
    parent_guardian_name VARCHAR(255),
    student_statement TEXT,
    evidence_presented JSON,
    witness_testimonies JSON,
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
    other_penalties JSON,
    decision_summary TEXT,
    decision_rationale TEXT,
    decision_recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decision_recorded_by BIGINT UNSIGNED NOT NULL,
    transcript_prepared BOOLEAN DEFAULT FALSE,
    transcript_url TEXT,
    followup_required BOOLEAN DEFAULT FALSE,
    followup_date DATE,
    followup_assigned_to BIGINT UNSIGNED,
    appeal_rights_explained BOOLEAN DEFAULT FALSE,
    appeal_rights_explained_by BIGINT UNSIGNED,
    appeal_deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_disciplinary (disciplinary_action_id),
    INDEX idx_dates (hearing_date, followup_date),
    INDEX idx_panel (decision_recorded_by),
    INDEX idx_appeal (appeal_deadline, appeal_rights_explained),
    FOREIGN KEY (disciplinary_action_id) REFERENCES school_disciplinary_actions(id) ON DELETE CASCADE,
    FOREIGN KEY (decision_recorded_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (followup_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Formal disciplinary hearing records and outcomes';

-- -----------------------------------------------------------------------------
-- 7.10 SCHOOL_STUDENT_HEALTH_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_student_health_records (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED UNIQUE NOT NULL, -- one record per student
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    bmi DECIMAL(4,2) GENERATED ALWAYS AS (weight_kg / POWER(height_cm/100, 2)) STORED,
    known_allergies JSON, -- ["peanuts", "penicillin"]
    chronic_illnesses JSON, -- ["asthma", "diabetes"]
    medications JSON, -- [{name: "inhaler", dosage: "2 puffs daily"}]
    regular_medications TEXT,
    emergency_medications TEXT,
    immunizations JSON, -- [{name: "MMR", date: "2020-01-15", booster: true}]
    last_physical_exam_date DATE,
    last_dental_checkup DATE,
    last_eye_checkup DATE,
    hearing_status ENUM('normal', 'impaired', 'deaf') DEFAULT 'normal',
    vision_status ENUM('normal', 'corrected', 'impaired', 'blind') DEFAULT 'normal',
    physical_limitations TEXT,
    dietary_restrictions JSON,
    mental_health_conditions JSON, -- ["anxiety", "ADHD"]
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
    last_updated_by BIGINT UNSIGNED,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    consent_for_treatment BOOLEAN DEFAULT FALSE,
    consent_for_emergency_care BOOLEAN DEFAULT FALSE,
    consent_for_sharing_info BOOLEAN DEFAULT FALSE,
    notes TEXT,
    INDEX idx_student (student_id),
    INDEX idx_blood (blood_group),
    INDEX idx_allergies (known_allergies), -- JSON search (depends on MySQL version)
    INDEX idx_chronic (chronic_illnesses),
    INDEX idx_sports_clearance (sports_clearance, sports_clearance_valid_until),
    INDEX idx_insurance (insurance_provider, insurance_policy_number),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (last_updated_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (height_cm > 0),
    CHECK (weight_kg > 0),
    CHECK (bmi BETWEEN 10 AND 50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Comprehensive student medical and health profile';

-- -----------------------------------------------------------------------------
-- 7.11 SCHOOL_VACCINATION_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vaccination_records (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    vaccine_name VARCHAR(255) NOT NULL,
    vaccine_type VARCHAR(100),
    dose_number INT UNSIGNED DEFAULT 1,
    total_doses_required INT UNSIGNED NOT NULL,
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
    exemption_granted_by BIGINT UNSIGNED,
    exemption_granted_at TIMESTAMP NULL,
    verified_by BIGINT UNSIGNED,
    verified_at TIMESTAMP NULL,
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_vaccine_dose (student_id, vaccine_name, dose_number),
    INDEX idx_student (student_id),
    INDEX idx_vaccine (vaccine_name),
    INDEX idx_dates (vaccination_date, next_due_date),
    INDEX idx_mandatory (is_mandatory),
    INDEX idx_verified (verified_by, verified_at),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (exemption_granted_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (dose_number >= 1 AND dose_number <= total_doses_required)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student immunization records and compliance';

-- -----------------------------------------------------------------------------
-- 7.12 SCHOOL_MEDICAL_VISITS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_medical_visits (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    visit_id CHAR(36) UNIQUE NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    visit_type ENUM('injury', 'illness', 'routine_checkup', 'medication', 'vaccination', 'mental_health', 'other') DEFAULT 'illness',
    presenting_complaint TEXT NOT NULL,
    symptoms_observed TEXT,
    vitals JSON, -- {"bp": "120/80", "temp": 98.6, "pulse": 72}
    treatment_provided LONGTEXT,
    medications_given JSON,
    bandage_applied BOOLEAN DEFAULT FALSE,
    injury_location VARCHAR(100),
    injury_severity ENUM('minor', 'moderate', 'severe') DEFAULT 'minor',
    referred_to_hospital BOOLEAN DEFAULT FALSE,
    hospital_name VARCHAR(255),
    referral_reason TEXT,
    parent_contacted BOOLEAN DEFAULT FALSE,
    parent_contacted_at TIMESTAMP NULL,
    parent_contact_method ENUM('phone', 'sms', 'email', 'messaging_app'),
    parent_response ENUM('acknowledged', 'coming_to_school', 'asked_to_go_home', 'no_response'),
    student_sent_home BOOLEAN DEFAULT FALSE,
    sent_home_reason TEXT,
    ambulance_called BOOLEAN DEFAULT FALSE,
    ambulance_service VARCHAR(255),
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    follow_up_notes TEXT,
    treated_by BIGINT UNSIGNED NOT NULL, -- school nurse/doctor
    case_notes LONGTEXT,
    is_confidential BOOLEAN DEFAULT FALSE,
    confidentiality_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_visit_id (visit_id),
    INDEX idx_student_date (student_id, visit_date),
    INDEX idx_visit_type (visit_type),
    INDEX idx_followup (follow_up_required, follow_up_date),
    INDEX idx_treated (treated_by),
    INDEX idx_created (created_at),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (treated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    CHECK (visit_time IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='School nurse/medical room visit logs';

-- -----------------------------------------------------------------------------
-- 7.13 (Bonus / optional) COLLEGE_STUDENT_SPECIAL_NEEDS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_student_special_needs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED UNIQUE NOT NULL,
    disability_type ENUM('physical', 'visual', 'hearing', 'learning', 'mental_health', 'chronic_illness', 'multiple') NOT NULL,
    disability_certificate_url TEXT,
    diagnosis_details TEXT,
    functional_limitations TEXT,
    required_accommodations JSON, -- ["extra_time", "scribe", "wheelchair_ramp"]
    current_accommodations JSON,
    recommended_by VARCHAR(255),
    recommendation_date DATE,
    reviewed_by BIGINT UNSIGNED,
    reviewed_date DATE,
    review_frequency_months INT DEFAULT 12,
    next_review_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_student (student_id),
    INDEX idx_disability (disability_type),
    INDEX idx_active (is_active),
    INDEX idx_review (next_review_date),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student special needs and accommodation requirements';

-- -----------------------------------------------------------------------------
-- 7.14 (Bonus / optional) SCHOOL_STUDENT_SAFETY_INCIDENTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_student_safety_incidents (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    incident_id CHAR(36) UNIQUE NOT NULL,
    incident_type ENUM('accident', 'near_miss', 'hazard', 'injury', 'property_damage', 'intentional_harm') DEFAULT 'accident',
    reported_by BIGINT UNSIGNED NOT NULL,
    incident_date DATE NOT NULL,
    incident_time TIME,
    location_type ENUM('classroom', 'corridor', 'playground', 'lab', 'canteen', 'toilet', 'bus', 'off_campus') DEFAULT 'classroom',
    specific_location VARCHAR(255),
    students_involved JSON, -- [{"student_id": 123, "role": "victim", "injury": "minor"}]
    staff_witnesses JSON, -- [teacher_id1, teacher_id2]
    description TEXT NOT NULL,
    root_cause_analysis TEXT,
    immediate_actions_taken TEXT,
    injuries_sustained BOOLEAN DEFAULT FALSE,
    injury_details JSON,
    medical_attention_required BOOLEAN DEFAULT FALSE,
    hospital_transport BOOLEAN DEFAULT FALSE,
    property_damage BOOLEAN DEFAULT FALSE,
    property_damage_value DECIMAL(12,2),
    police_involved BOOLEAN DEFAULT FALSE,
    police_report_filed BOOLEAN DEFAULT FALSE,
    police_report_number VARCHAR(100),
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notified_at TIMESTAMP NULL,
    parent_contact_details JSON,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_assigned_to BIGINT UNSIGNED,
    follow_up_due_date DATE,
    status ENUM('open', 'investigating', 'resolved', 'closed') DEFAULT 'open',
    closed_at TIMESTAMP NULL,
    closed_by BIGINT UNSIGNED,
    preventive_measures TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_incident_id (incident_id),
    INDEX idx_dates (incident_date, follow_up_due_date),
    INDEX idx_reporter (reported_by),
    INDEX idx_status (status),
    INDEX idx_type (incident_type),
    INDEX idx_location (location_type, specific_location(255)),
    INDEX idx_followup (follow_up_required, follow_up_assigned_to),
    FOREIGN KEY (reported_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (follow_up_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (closed_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student safety incident reports and investigations';

-- ============================================================================
-- PLAN 7 COMPLETE: 12 tables created successfully
-- (14 including welfare enrollment + safety incidents extensions)
-- ============================================================================
