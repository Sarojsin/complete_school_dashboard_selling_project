"""
Tests for College Account Section Module

Covers faculty payment management functionality.
"""

import pytest
from decimal import Decimal
from modules.college.college_account_section.service import AccountService
from modules.college.college_account_section.schemas import (
    CollegePaymentCreate, CollegePaymentUpdate, CollegePaymentResponse
)
from modules.college.college_account_section.models import CollegeFacultyPayment
from modules.shared.exceptions import NotFoundError, ValidationError
from modules.shared.models import UserRole
from tests.factories import create_faculty, create_department


pytestmark = pytest.mark.asyncio


class TestAccountService:
    """Service layer unit tests"""

    async def test_record_payment_success(self, async_db, create_user_and_token):
        """Test recording a payment successfully"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05",
            payment_type="salary",
            payment_method="bank_transfer",
            transaction_reference="TXN123456",
            remarks="Monthly salary"
        )

        response = await service.record_payment(payment_data, recorded_by=user.id)
        payment = response["payment"]

        assert payment.faculty_id == faculty.id
        assert payment.amount == 50000.0
        assert payment.month == "2024-05"
        assert payment.payment_type.value == "salary"
        assert payment.paid_by_user_id == user.id

    async def test_record_payment_invalid_amount(self, async_db, create_user_and_token):
        """Test recording payment with negative amount raises ValidationError"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=-100.0,  # Invalid negative amount
            month="2024-05",
            payment_type="salary"
        )

        with pytest.raises(ValidationError):
            await service.record_payment(payment_data, recorded_by=user.id)

    async def test_get_all_payments(self, async_db, create_user_and_token):
        """Test getting all payments"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)

        # Create multiple payments
        payments_data = [
            CollegePaymentCreate(faculty_id=faculty.id, amount=50000.0, month="2024-05"),
            CollegePaymentCreate(faculty_id=faculty.id, amount=55000.0, month="2024-06"),
        ]

        for data in payments_data:
            await service.record_payment(data, recorded_by=user.id)

        payments = await service.get_all_payments()
        assert len(payments) >= 2

        # Test filtering by faculty
        faculty_payments = await service.get_all_payments(faculty_id=faculty.id)
        assert len(faculty_payments) >= 2

        # Test filtering by month
        may_payments = await service.get_all_payments(month="2024-05")
        assert len(may_payments) >= 1
        assert may_payments[0].month == "2024-05"

    async def test_get_teacher_payments(self, async_db, create_user_and_token):
        """Test getting payments for a specific faculty member"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)

        # Create payments
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        await service.record_payment(payment_data, recorded_by=user.id)

        payments = await service.get_teacher_payments(faculty.id)
        assert len(payments) >= 1
        assert payments[0].faculty_id == faculty.id

    async def test_get_payment_detail(self, async_db, create_user_and_token):
        """Test getting single payment detail"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        detail_response = await service.get_payment_detail(payment_id)
        payment = detail_response["payment"]

        assert payment.id == payment_id
        assert payment.amount == 50000.0

    async def test_get_payment_detail_not_found(self, async_db):
        """Test getting payment detail for non-existent payment"""
        service = AccountService(async_db)

        with pytest.raises(NotFoundError):
            await service.get_payment_detail(99999)

    async def test_update_payment(self, async_db, create_user_and_token):
        """Test updating payment details"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05",
            remarks="Original remarks"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        update_data = CollegePaymentUpdate(
            transaction_reference="NEW_TXN_123",
            remarks="Updated remarks"
        )

        update_response = await service.update_payment(payment_id, update_data)
        updated_payment = update_response["payment"]

        assert updated_payment.transaction_reference == "NEW_TXN_123"
        assert updated_payment.remarks == "Updated remarks"

    async def test_delete_payment(self, async_db, create_user_and_token):
        """Test deleting payment record"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        # Verify payment exists
        detail_response = await service.get_payment_detail(payment_id)
        assert detail_response["payment"].id == payment_id

        # Delete payment
        delete_response = await service.delete_payment(payment_id)
        assert delete_response["message"] == "Payment record deleted successfully"

        # Verify payment is gone
        with pytest.raises(NotFoundError):
            await service.get_payment_detail(payment_id)

    async def test_get_account_stats(self, async_db, create_user_and_token):
        """Test getting account section statistics"""
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        service = AccountService(async_db)

        # Create some payments
        payments_data = [
            CollegePaymentCreate(faculty_id=faculty.id, amount=50000.0, month="2024-05"),
            CollegePaymentCreate(faculty_id=faculty.id, amount=55000.0, month="2024-06"),
        ]

        for data in payments_data:
            await service.record_payment(data, recorded_by=user.id)

        stats_response = await service.get_account_stats()
        stats = stats_response["stats"]

        assert stats.total_payments >= 2
        assert stats.total_amount >= 105000.0
        assert stats.faculty_count >= 1


class TestAccountAPI:
    """API integration tests"""

    async def test_record_payment_requires_account_role(self, async_client, create_user_and_token):
        """Test that recording payment requires account section role"""
        student, headers = await create_user_and_token(role=UserRole.COLLEGE_STUDENT)

        payload = {
            "faculty_id": 1,
            "amount": 50000.0,
            "month": "2024-05",
            "payment_type": "salary"
        }

        resp = await async_client.post("/api/v1/college/account/payments", json=payload, headers=headers)
        assert resp.status_code == 403

    async def test_record_payment_success(self, async_client, async_db, create_user_and_token):
        """Test recording payment via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        payload = {
            "faculty_id": faculty.id,
            "amount": 50000.0,
            "month": "2024-05",
            "payment_type": "salary",
            "payment_method": "bank_transfer",
            "transaction_reference": "TXN123456",
            "remarks": "Monthly salary"
        }

        resp = await async_client.post("/api/v1/college/account/payments", json=payload, headers=headers)
        assert resp.status_code == 201

        data = resp.json()
        assert data["payment"]["faculty_id"] == faculty.id
        assert data["payment"]["amount"] == 50000.0
        assert data["payment"]["month"] == "2024-05"

    async def test_get_all_payments_requires_auth(self, async_client):
        """Test that getting payments requires authentication"""
        resp = await async_client.get("/api/v1/college/account/payments")
        assert resp.status_code == 401

    async def test_get_all_payments_success(self, async_client, async_db, create_user_and_token):
        """Test getting all payments via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        # Create a payment
        from modules.college.college_account_section.service import AccountService
        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        await service.record_payment(payment_data, recorded_by=user.id)

        resp = await async_client.get("/api/v1/college/account/payments", headers=headers)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) >= 1

    async def test_get_payment_detail(self, async_client, async_db, create_user_and_token):
        """Test getting single payment detail via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        # Create a payment
        from modules.college.college_account_section.service import AccountService
        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        resp = await async_client.get(f"/api/v1/college/account/payments/{payment_id}", headers=headers)
        assert resp.status_code == 200

        data = resp.json()
        assert data["payment"]["id"] == payment_id

    async def test_update_payment(self, async_client, async_db, create_user_and_token):
        """Test updating payment via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        # Create a payment
        from modules.college.college_account_section.service import AccountService
        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05",
            remarks="Original remarks"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        update_payload = {
            "transaction_reference": "UPDATED_TXN_123",
            "remarks": "Updated remarks"
        }

        resp = await async_client.patch(f"/api/v1/college/account/payments/{payment_id}",
                                       json=update_payload, headers=headers)
        assert resp.status_code == 200

        data = resp.json()
        assert data["payment"]["transaction_reference"] == "UPDATED_TXN_123"
        assert data["payment"]["remarks"] == "Updated remarks"

    async def test_delete_payment(self, async_client, async_db, create_user_and_token):
        """Test deleting payment via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)
        dept = await create_department(async_db, "Computer Science", "CS")
        faculty = await create_faculty(async_db, user.id, dept.id)

        # Create a payment
        from modules.college.college_account_section.service import AccountService
        service = AccountService(async_db)
        payment_data = CollegePaymentCreate(
            faculty_id=faculty.id,
            amount=50000.0,
            month="2024-05"
        )
        created_response = await service.record_payment(payment_data, recorded_by=user.id)
        payment_id = created_response["payment"].id

        resp = await async_client.delete(f"/api/v1/college/account/payments/{payment_id}", headers=headers)
        assert resp.status_code == 204

        # Verify payment is gone
        resp2 = await async_client.get(f"/api/v1/college/account/payments/{payment_id}", headers=headers)
        assert resp2.status_code == 404

    async def test_get_account_stats(self, async_client, create_user_and_token):
        """Test getting account stats via API"""
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)

        resp = await async_client.get("/api/v1/college/account/stats", headers=headers)
        assert resp.status_code == 200

        data = resp.json()
        assert "stats" in data
        assert "total_payments" in data["stats"]