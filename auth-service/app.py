"""
Authentication Service API
ENMS Demo Platform
Created: December 11, 2025
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_service import (
    register_user,
    login_user,
    verify_email_token,
    request_password_reset,
    reset_password,
    require_admin,
    get_db_connection,
    verify_token,
    submit_pilot_factory_application,
    send_pilot_factory_confirmation_email,
    send_pilot_factory_admin_notification
)
from psycopg2.extras import RealDictCursor
import logging
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Configure appropriately for production
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ============================================================================
# Health Check
# ============================================================================

@app.route('/api/auth/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'auth-service',
        'status': 'healthy'
    }), 200

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    """Register new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'organization', 'full_name', 'position', 'country']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        result = register_user(
            email=data['email'],
            password=data['password'],
            organization=data['organization'],
            full_name=data['full_name'],
            position=data['position'],
            mobile=data.get('mobile', ''),
            country=data['country'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Registration endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Registration failed'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        result = login_user(
            email=data['email'],
            password=data['password'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        status_code = 200 if result['success'] else 401
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Login endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Login failed'
        }), 500

@app.route('/api/auth/verify-email', methods=['POST'])
def auth_verify_email():
    """Verify email with token"""
    try:
        data = request.get_json()
        
        if not data.get('token'):
            return jsonify({
                'success': False,
                'error': 'Verification token is required'
            }), 400
        
        result = verify_email_token(data['token'])
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Email verification endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Verification failed'
        }), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def auth_forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        result = request_password_reset(data['email'])
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Forgot password endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Request failed'
        }), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def auth_reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        
        if not data.get('token') or not data.get('new_password'):
            return jsonify({
                'success': False,
                'error': 'Token and new password are required'
            }), 400
        
        result = reset_password(data['token'], data['new_password'])
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Reset password endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Password reset failed'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    """Logout user (invalidate session)"""
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'No authorization token'
            }), 401
        
        token = auth_header.split(' ')[1]
        token_data = verify_token(token)
        
        if token_data['valid']:
            # Invalidate session in database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE demo_sessions 
                SET is_active = false 
                WHERE session_token = %s
            """, (token,))
            conn.commit()
            cursor.close()
            conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Logout endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500

@app.route('/api/auth/verify-token', methods=['POST'])
def auth_verify_token():
    """Verify JWT token validity"""
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'valid': False,
                'error': 'No authorization token'
            }), 401
        
        token = auth_header.split(' ')[1]
        token_data = verify_token(token)
        
        if token_data['valid']:
            return jsonify({
                'success': True,
                'valid': True,
                'user': token_data['payload']
            }), 200
        else:
            return jsonify({
                'success': False,
                'valid': False,
                'error': token_data['error']
            }), 401
            
    except Exception as e:
        logger.error(f"Token verification endpoint error: {e}")
        return jsonify({
            'success': False,
            'valid': False,
            'error': 'Verification failed'
        }), 500

# ============================================================================
# Admin Endpoints
# ============================================================================

@app.route('/api/admin/stats', methods=['GET'])
@require_admin
def admin_get_stats():
    """Get user statistics (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_users,
                COUNT(*) FILTER (WHERE email_verified = true) as verified_users,
                COUNT(*) FILTER (WHERE DATE(created_at) = CURRENT_DATE) as new_today,
                COUNT(*) FILTER (WHERE last_login >= NOW() - INTERVAL '7 days') as active_7_days,
                COUNT(*) FILTER (WHERE role = 'admin') as admin_users
            FROM demo_users
            WHERE is_active = true
        """)
        
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': dict(stats)
        }), 200
        
    except Exception as e:
        logger.error(f"Admin stats endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch statistics'
        }), 500

@app.route('/api/admin/users', methods=['GET'])
@require_admin
def admin_get_users():
    """Get paginated user list with search (admin only)"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        search = request.args.get('search', '').strip()
        
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Build query with search
        where_clause = ""
        params = []
        
        if search:
            where_clause = """
                WHERE (full_name ILIKE %s OR email ILIKE %s OR organization ILIKE %s)
            """
            search_pattern = f'%{search}%'
            params = [search_pattern, search_pattern, search_pattern]
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM demo_users {where_clause}"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']
        
        # Get users
        users_query = f"""
            SELECT id, email, full_name, organization, position, mobile, country,
                   email_verified, role, created_at, last_login, is_active
            FROM demo_users
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(users_query, params + [limit, offset])
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert datetime objects to ISO format
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()
            if user['last_login']:
                user['last_login'] = user['last_login'].isoformat()
        
        total_pages = (total_count + limit - 1) // limit
        
        return jsonify({
            'success': True,
            'users': users,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Admin users endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch users'
        }), 500

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
@require_admin
def admin_get_user(user_id):
    """Get detailed user information (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, email, full_name, organization, position, mobile, country,
                   email_verified, verified_at, role, created_at, last_login, is_active,
                   ip_address_signup, deactivated_at
            FROM demo_users
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get user's sessions
        cursor.execute("""
            SELECT id, created_at, expires_at, last_activity, ip_address, is_active
            FROM demo_sessions
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 10
        """, (user_id,))
        
        sessions = cursor.fetchall()
        
        # Get user's audit log
        cursor.execute("""
            SELECT action, status, timestamp, ip_address, metadata
            FROM demo_audit_log
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT 20
        """, (user_id,))
        
        audit_logs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert datetime objects to ISO format
        for key in ['created_at', 'last_login', 'verified_at', 'deactivated_at']:
            if user.get(key):
                user[key] = user[key].isoformat()
        
        for session in sessions:
            for key in ['created_at', 'expires_at', 'last_activity']:
                if session.get(key):
                    session[key] = session[key].isoformat()
        
        for log in audit_logs:
            if log.get('timestamp'):
                log['timestamp'] = log['timestamp'].isoformat()
        
        return jsonify({
            'success': True,
            'user': dict(user),
            'sessions': [dict(s) for s in sessions],
            'audit_logs': [dict(l) for l in audit_logs]
        }), 200
        
    except Exception as e:
        logger.error(f"Admin get user endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch user details'
        }), 500

@app.route('/api/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@require_admin
def admin_toggle_user_active(user_id):
    """Activate/deactivate user account (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT is_active FROM demo_users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        new_status = not user['is_active']
        deactivated_at = 'NOW()' if not new_status else 'NULL'
        
        cursor.execute(f"""
            UPDATE demo_users
            SET is_active = %s, deactivated_at = {deactivated_at}
            WHERE id = %s
        """, (new_status, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        action = 'activated' if new_status else 'deactivated'
        
        return jsonify({
            'success': True,
            'message': f'User {action} successfully',
            'is_active': new_status
        }), 200
        
    except Exception as e:
        logger.error(f"Admin toggle user endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to update user status'
        }), 500

@app.route('/api/admin/export-users', methods=['GET'])
@require_admin
def admin_export_users():
    """Export users to CSV (admin only)"""
    try:
        import csv
        from io import StringIO
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, email, full_name, organization, position, mobile, country,
                   email_verified, role, created_at, last_login, is_active
            FROM demo_users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Create CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'email', 'full_name', 'organization', 'position', 'mobile', 
            'country', 'email_verified', 'role', 'created_at', 'last_login', 'is_active'
        ])
        writer.writeheader()
        
        for user in users:
            user_dict = dict(user)
            if user_dict['created_at']:
                user_dict['created_at'] = user_dict['created_at'].isoformat()
            if user_dict['last_login']:
                user_dict['last_login'] = user_dict['last_login'].isoformat()
            writer.writerow(user_dict)
        
        csv_content = output.getvalue()
        output.close()
        
        from flask import make_response
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=users_export.csv'
        
        return response
        
    except Exception as e:
        logger.error(f"Admin export endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to export users'
        }), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================================================
# Pilot Factory Application Endpoints
# ============================================================================

# Rate limiting storage (in-memory, simple implementation)
# For production, use Redis or a proper rate limiting library
submission_tracker = defaultdict(list)

def check_rate_limit(ip_address: str, max_requests: int = 3, window_hours: int = 1) -> bool:
    """Check if IP has exceeded rate limit"""
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=window_hours)
    
    # Clean old entries
    submission_tracker[ip_address] = [
        timestamp for timestamp in submission_tracker[ip_address]
        if timestamp > cutoff
    ]
    
    # Check if limit exceeded
    if len(submission_tracker[ip_address]) >= max_requests:
        return False
    
    # Add current request
    submission_tracker[ip_address].append(now)
    return True

@app.route('/api/auth/pilot-factory-apply', methods=['POST'])
def pilot_factory_apply():
    """Submit pilot factory application"""
    try:
        # Get client IP (handle proxy headers)
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            ip_address = request.remote_addr
        
        # Check rate limiting
        if not check_rate_limit(ip_address):
            return jsonify({
                'success': False,
                'error': 'Too many submission attempts. Please try again in one hour.',
                'code': 'RATE_LIMIT_EXCEEDED'
            }), 429
        
        # Get form data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Get user agent
        user_agent = request.headers.get('User-Agent', '')
        
        # Submit application
        result = submit_pilot_factory_application(data, ip_address, user_agent)
        
        if not result['success']:
            # Handle specific error codes
            if result.get('code') == 'DUPLICATE_EMAIL':
                return jsonify(result), 409  # Conflict
            else:
                return jsonify(result), 400  # Bad Request
        
        # Send emails (Phase 3)
        # Prepare email data with formatted submission date
        email_data = {
            'application_ref': result['application_ref'],
            'application_id': result['application_id'],
            'company_name': result['company_name'],
            'contact_name': data.get('contact_name', ''),
            'contact_email': result['contact_email'],
            'contact_position': data.get('contact_position', ''),
            'contact_phone': data.get('contact_phone', ''),
            'city_address': data.get('city_address', ''),
            'manufacturing_sector': data.get('manufacturing_sector', ''),
            'num_employees': data.get('num_employees', ''),
            'facility_area': data.get('facility_area', ''),
            'annual_electricity': data.get('annual_electricity', ''),
            'num_production_operations': data.get('num_production_operations', ''),
            'digital_monitoring': data.get('digital_monitoring', False),
            'num_digital_meters': data.get('num_digital_meters', ''),
            'has_scada': data.get('has_scada', False),
            'has_energy_responsible': data.get('has_energy_responsible', ''),
            'digital_maturity': data.get('digital_maturity', ''),
            'willing_to_participate': data.get('willing_to_participate', False),
            'confirms_collaboration': data.get('confirms_collaboration', False),
            'preferred_meeting_week': data.get('preferred_meeting_week', ''),
            'preferred_installation_week': data.get('preferred_installation_week', ''),
            'ip_address': ip_address,
            'user_agent': user_agent,
            'submission_date': result['submitted_at']
        }
        
        # Send confirmation email to applicant (don't block on failure)
        try:
            send_pilot_factory_confirmation_email(email_data)
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {e}")
        
        # Send notification email to admins (don't block on failure)
        try:
            send_pilot_factory_admin_notification(email_data)
        except Exception as e:
            logger.error(f"Failed to send admin notification: {e}")
        
        logger.info(f"Pilot factory application submitted successfully: {result['application_ref']}")
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Pilot factory application endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your application. Please try again later.'
        }), 500

@app.route('/api/auth/admin/pilot-applications', methods=['GET'])
@require_admin
def get_pilot_applications():
    """Get list of pilot factory applications (admin only)"""
    try:
        # Get query parameters
        status_filter = request.args.get('status', '')
        maturity_filter = request.args.get('digital_maturity', '')
        search_query = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        sort_by = request.args.get('sort', 'submitted_at')
        sort_order = request.args.get('order', 'DESC')
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Build query
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Base query
        where_clauses = []
        params = []
        
        if status_filter:
            where_clauses.append("status = %s")
            params.append(status_filter)
        
        if maturity_filter:
            # Normalize maturity filter to match database values
            if maturity_filter.lower() == 'low':
                where_clauses.append("digital_maturity ILIKE %s")
                params.append("%low%")
            elif maturity_filter.lower() == 'medium':
                where_clauses.append("digital_maturity ILIKE %s")
                params.append("%medium%")
            elif maturity_filter.lower() == 'high':
                where_clauses.append("digital_maturity ILIKE %s")
                params.append("%high%")
        
        if search_query:
            where_clauses.append(
                "(company_name ILIKE %s OR contact_email ILIKE %s OR contact_name ILIKE %s)"
            )
            search_param = f"%{search_query}%"
            params.extend([search_param, search_param, search_param])
        
        where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Get total count
        cursor.execute(f"""
            SELECT COUNT(*) as total
            FROM pilot_factory_applications
            {where_sql}
        """, params)
        total_count = cursor.fetchone()['total']
        
        # Get applications
        cursor.execute(f"""
            SELECT 
                id, application_ref, company_name, contact_name, contact_email,
                contact_phone, manufacturing_sector, annual_electricity,
                digital_maturity, status, submitted_at, reviewed_at
            FROM pilot_factory_applications
            {where_sql}
            ORDER BY {sort_by} {sort_order}
            LIMIT %s OFFSET %s
        """, params + [limit, offset])
        
        applications = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'applications': applications,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching pilot applications: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch applications'
        }), 500

@app.route('/api/auth/admin/pilot-applications/<int:app_id>', methods=['GET'])
@require_admin
def get_pilot_application_detail(app_id):
    """Get detailed pilot factory application (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                pfa.*,
                du.full_name as reviewed_by_name
            FROM pilot_factory_applications pfa
            LEFT JOIN demo_users du ON pfa.reviewed_by = du.id
            WHERE pfa.id = %s
        """, (app_id,))
        
        application = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404
        
        return jsonify({
            'success': True,
            'application': application
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching pilot application detail: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch application details'
        }), 500

@app.route('/api/auth/admin/pilot-applications/<int:app_id>', methods=['PUT'])
@require_admin
def update_pilot_application(app_id):
    """Update pilot factory application status and notes (admin only)"""
    try:
        data = request.get_json()
        
        # Get admin user ID from token
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '')
        
        from auth_service import JWT_SECRET
        import jwt
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        admin_id = decoded['user_id']
        
        # Update application
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE pilot_factory_applications
            SET status = COALESCE(%s, status),
                admin_notes = COALESCE(%s, admin_notes),
                reviewed_by = %s,
                reviewed_at = NOW()
            WHERE id = %s
            RETURNING id, application_ref, status
        """, (
            data.get('status'),
            data.get('admin_notes'),
            admin_id,
            app_id
        ))
        
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Pilot application {result[1]} updated by admin {admin_id}")
        
        return jsonify({
            'success': True,
            'message': 'Application updated successfully',
            'application_id': result[0],
            'application_ref': result[1],
            'status': result[2]
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating pilot application: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to update application'
        }), 500

@app.route('/api/auth/admin/pilot-applications/stats', methods=['GET'])
@require_admin
def get_pilot_applications_stats():
    """Get pilot factory applications statistics (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'under_review' THEN 1 END) as under_review,
                COUNT(CASE WHEN status = 'reviewed' THEN 1 END) as reviewed,
                COUNT(CASE WHEN status = 'accepted' THEN 1 END) as accepted,
                COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected
            FROM pilot_factory_applications
        """)
        
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching pilot applications stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch statistics'
        }), 500

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('AUTH_SERVICE_PORT', 5000))
    debug = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
    
    logger.info(f"Starting Auth Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
