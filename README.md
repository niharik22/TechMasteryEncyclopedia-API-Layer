# Tech Mastery Encyclopedia

**Master the skills & Shape your future**  
Stay ready for the future. Discover the skills that matter most and gain the insights to grow and seize new opportunities with confidence. The Tech Mastery Encyclopedia project is dedicated to empowering individuals by identifying in-demand skills through advanced data analysis and machine learning.

---

# API Layer

### Architecture Overview
The API Layer is built using **FastAPI** to provide seamless integration between data processing components and the presentation layer. The system ensures efficient delivery of processed insights to the front-end, enabling interactive data exploration.

**Explore Other Components**:
- [Visit the Website](https://techmasteryencyclopedia.com/) - Experience the live application.
- [Machine Learning Layer](https://github.com/niharik22/TechMasteryEncyclopedia-MachineLearning-Layer) - Advanced data analysis and model implementation.
- [Presentation Layer](https://github.com/niharik22/TechMasteryEncyclopedia-Presentation-Layer) - User-friendly visualizations and dashboards.


#### Deployment and Hosting

The **API Layer** has been containerized using **Docker** and is hosted on **AWS EC2**, ensuring consistent and reliable performance. This cloud-based infrastructure provides high availability and scalability, supporting the seamless integration and delivery of data insights to the presentation layer.

- **Docker Implementation**: The entire API is fully containerized, facilitating efficient and standardized deployment.
- **AWS EC2 Deployment**: Leveraging the power of AWS EC2 for cloud hosting, providing a robust environment for the API.


### Security & Authentication
- **Method**: HTTP Basic Authentication
- **Credential Management**: Environment variable-based configuration for storing sensitive credentials securely
- **Access Control**: All API endpoints are protected, requiring proper authentication to access
- **CORS Configuration**: Configured Cross-Origin Resource Sharing (CORS) to allow controlled access from different domains during testing, with plans to restrict in production for enhanced security


### API Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns API status confirmation
```json
{
    "message": "Welcome to the Tech Mastery API"
}
```

#### 2. Operations Details
```
POST /details/operations
```
**Purpose**: Retrieve role-specific tools, skills, libraries, and languages  
**Authentication**: Required  
**Request Format**:
```json
{
    "country": "United States",
    "state": "CA",
    "role": "Data Engineer"
}
```

#### 3. Education Details
```
POST /details/education
```
**Purpose**: Access education-related insights  
**Authentication**: Required  
**Request Body**: FullRequestData

#### 4. Workplace Analysis
```
POST /details/workplace
```
**Purpose**: Obtain workplace arrangement statistics  
**Authentication**: Required  
**Request Body**: FullRequestData

#### 5. Country Information
```
POST /details/country
```
**Purpose**: Retrieve state-specific information  
**Authentication**: Required  
**Request Body**: CountryOnlyRequest

#### 6. Available Roles
```
POST /details/roles
```
**Purpose**: Get list of available roles by country  
**Authentication**: Required  
**Request Body**: CountryOnlyRequest

## Data Processing Architecture

### Core Components

#### QualifiedService Class
Manages MongoDB interactions for data retrieval and aggregation.

**Key Methods**:
- `get_place_of_work_count_grouped_by_role_and_state()`
- `get_bigram_details_by_country_state_role()`
- `get_education_data_by_country_state_role()`
- `get_freq_grouped_by_state()`
- `get_roles_by_country_and_state()`

#### DataProcessor Class
Handles data transformation and preparation for API responses.

**Key Methods**:
- `process_place_of_work_data()`: Workplace statistics calculation
- `process_tools_data()`: Tool usage analysis
- `process_skills_data()`: Skill requirement processing
- `process_languages_data()`: Programming language analysis
- `process_libraries_data()`: Framework usage statistics
- `process_bigram_data()`: Comprehensive data aggregation
- `process_education_data()`: Education requirement analysis
- `process_state_frequency_data()`: Geographic distribution calculation
- `fetch_distinct_roles()`: Role availability mapping

### Data Flow
1. Ingestion of processed data from the Machine Learning layer, specifically from the Bigram analysis results stored in MongoDB
2. Processing and enrichment of data using `DataProcessor` methods to extract and format insights such as tools, skills, libraries, and languages
3. Transformation of these insights into standardized response formats suitable for API delivery
4. Delivery of structured and enriched data through secure API endpoints for client consumption


markdown
Copy code
### Testing & Quality Assurance

The API layer includes a comprehensive testing suite to ensure the functionality, reliability, and accuracy of all components. The testing framework uses `unittest` to cover various aspects of the service, including data retrieval and processing.

#### Testing Strategy

1. **Unit Tests**
   - Ensure that individual components, such as service methods and data processing functions, work as expected.
   - Validate MongoDB queries and data transformation logic.

2. **Mocking MongoDB**
   - Uses `unittest.mock` to create mock instances of the `MongoDBClient` to simulate database interactions without needing a live database.
   - Ensures consistent test results and isolates the logic from external dependencies.

3. **Test Cases**
   - **Place of Work Count**: Tests the aggregation of workplace counts for a given role, state, and country.
   - **Bigram Data Retrieval**: Verifies that tools, libraries, skills, and languages are correctly fetched and formatted from the bigram data.
   - **Education Data**: Checks the accuracy of education-related data retrieval and formatting.
   - **State Frequency Data**: Validates the correct grouping and percentage calculation of records by state.
   - **Role Retrieval**: Tests the distinct role retrieval functionality to ensure it returns expected results.
   
   ---


**Visit the Live Project**: [Link to the Website](https://techmasteryencyclopedia.com/)
