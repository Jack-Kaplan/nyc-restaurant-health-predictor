# Restaurant Inspection Data Dictionary

## Dataset Information

### General

| Field | Value |
|-------|-------|
| **Dataset Name** | Restaurant Inspection Data |
| **Agency Name** | DOHMH |
| **Update Frequency** | Daily |
| **Dataset Keywords** | Restaurants, Food Safety, Grades, Inspections |
| **Dataset Category** | Health |

### Detailed Description

The dataset contains current inspection data for permitted restaurants and college cafeterias (hereafter, restaurants) in NYC. All restaurants are required to be in compliance with NYS and NYC Food Safety Regulations, found in New York City Health Code Article 81. Restaurant inspections are conducted at least annually to ensure compliance with food safety regulations. This data set includes information obtained as part of the permitting process and data collected during inspections. This data includes inspection results for active restaurants for the last three years. Inactive restaurants and any violations cited during the inspection that were dismissed during adjudication are excluded.

---

## Column Descriptions

### CAMIS
- **Description:** Unique identifier for the establishment (restaurant)
- **Format:** 10-digit integer, static per restaurant permit

### DBA
- **Description:** Establishment (restaurant) name
- **Definition:** DBA = Doing Business As
- **Notes:** Public business name, may change at discretion of restaurant owner

### BORO
- **Description:** Borough of establishment (restaurant) location
- **Valid Values:**
  - 1 = MANHATTAN
  - 2 = BRONX
  - 3 = BROOKLYN
  - 4 = QUEENS
  - 5 = STATEN ISLAND
  - Missing
- **Notes:** There may be discrepancies between zip code and listed boro due to differences in an establishment's mailing address and physical location

### BUILDING
- **Description:** Building number for establishment (restaurant) location

### STREET
- **Description:** Street name for establishment (restaurant) location

### ZIPCODE
- **Description:** Zip code of establishment (restaurant) location

### PHONE
- **Description:** Phone number
- **Notes:** Phone number provided by restaurant owner/manager

### CUISINE DESCRIPTION
- **Description:** Establishment (restaurant) cuisine
- **Notes:** Optional field provided by restaurant owner/manager

### INSPECTION DATE
- **Description:** Date of inspection
- **Notes:** Inspection dates of 1/1/1900 mean an establishment has not yet had an inspection

### ACTION
- **Description:** Action associated with each establishment (restaurant) inspection
- **Valid Values:**
  - Violations were cited in the following area(s).
  - No violations were recorded at the time of this inspection.
  - Establishment re-opened by DOHMH
  - Establishment re-closed by DOHMH
  - Establishment Closed by DOHMH. Violations were cited in the following area(s) and those requiring immediate action were addressed.
  - "Missing" = not yet inspected

### VIOLATION CODE
- **Description:** Violation code associated with an establishment (restaurant) inspection

### VIOLATION DESCRIPTION
- **Description:** Violation description associated with an establishment (restaurant) inspection

### CRITICAL FLAG
- **Description:** Indicator of critical violation
- **Valid Values:**
  - Critical
  - Not Critical
  - Not Applicable
- **Notes:** Critical violations are those most likely to contribute to foodborne illness

### SCORE
- **Description:** Total score for a particular inspection
- **Notes:** Scores are updated based on adjudication results

### GRADE
- **Description:** Grade associated with the inspection
- **Valid Values:**
  - N = Not Yet Graded
  - A = Grade A
  - B = Grade B
  - C = Grade C
  - Z = Grade Pending
  - P = Grade Pending issued on re-opening following an initial inspection that resulted in a closure
- **Notes:** Grades given during a reopening inspection are derived from the previous re-inspection

### GRADE DATE
- **Description:** Date when grade was issued to the establishment (restaurant)

### RECORD DATE
- **Description:** Date record was added to dataset
- **Notes:** Dataset updated daily

### INSPECTION TYPE
- **Description:** A combination of the inspection program and the type of inspection performed
- **Valid Values:**
  - Calorie Posting/Compliance Inspection
  - Calorie Posting/Initial Inspection
  - Calorie Posting/Re-Inspection
  - Calorie Posting/Second Compliance Inspection
  - Cycle Inspection/Compliance Inspection
  - Cycle Inspection/Initial Inspection
  - Cycle Inspection/Re-Inspection
  - Cycle Inspection/Reopening Inspection
  - Cycle Inspection/Second Compliance Inspection
  - Inter-Agency Task Force/Initial Inspection
  - Inter-Agency Task Force/Re-Inspection
  - Pre-Permit (Non-operational)/Compliance Inspection
  - Pre-Permit (Non-operational)/Initial Inspection
  - Pre-Permit (Non-operational)/Re-Inspection
  - Pre-Permit (Non-operational)/Second Compliance Inspection
  - Pre-Permit(Operational)/Compliance Inspection
  - Pre-Permit(Operational)/Initial Inspection
  - Pre-Permit(Operational)/Re-Inspection
  - Pre-Permit(Operational)/Reopening Inspection
  - Pre-Permit(Operational)/Second Compliance Inspection
  - Smoke-Free Air Act/Complaint (Initial Inspection)
  - Smoke-Free Air Act/Compliance Inspection
  - Smoke-Free Air Act/Initial Inspection
  - Smoke-Free Air Act/Limited Inspection
  - Smoke-Free Air Act/Re-inspection
  - Smoke-Free Air Act/Second Compliance Inspection
  - Trans Fat/Compliance Inspection
  - Trans Fat/Initial Inspection
  - Trans Fat/Re-inspection
  - Trans Fat/Second Compliance Inspection

---

## Dataset Revision History

| Version | Date | Change Highlights | Comments |
|---------|------|-------------------|----------|
| - | - | - | - |

---

## Reference: Valid Values

### Update Frequency Options
- Annually
- Biannually
- Triannually
- Quarterly
- Monthly
- Bimonthly
- Weekly
- Biweekly
- Daily
- Several times per day
- As needed
- Historical

### Dataset Category Options
- Business
- City Government
- Education
- Environment
- Health
- Housing & Development
- Public Safety
- Recreation
- Social Services
- Transportation

---

*Form Version 1.0*
