package com.smartparking.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "customer_parking")
public class CustomerParkingEntity {
	
	@Id
	private String id;
	
	@Field(value = "license_plate")
	private String license_plate ;
	
	@Field(value="date_check_in")
	private String date_check_in;
	
	@Field(value="date_check_out")
	private String date_check_out;
	
	@Field(value="status")
	private boolean status;
	
	@Field(value ="fee")
	private int fee;
	
	private CustomerEntity customer;
	
	

	public CustomerParkingEntity() {
		super();
	}



	public CustomerParkingEntity(String license_plate, String date_check_in, String date_check_out, boolean status, int fee,
			CustomerEntity customer) {
		super();
		this.license_plate = license_plate;
		this.date_check_in = date_check_in;
		this.date_check_out = date_check_out;
		this.status = status;
		this.fee = fee;
		this.customer = customer;
	}



	public String getLicense_plate() {
		return license_plate;
	}



	public void setLicense_plate(String license_plate) {
		this.license_plate = license_plate;
	}






	public String getId() {
		return id;
	}



	public void setId(String id) {
		this.id = id;
	}



	public String getDate_check_in() {
		return date_check_in;
	}



	public void setDate_check_in(String date_check_in) {
		this.date_check_in = date_check_in;
	}



	public String getDate_check_out() {
		return date_check_out;
	}



	public void setDate_check_out(String date_check_out) {
		this.date_check_out = date_check_out;
	}



	public boolean isStatus() {
		return status;
	}



	public void setStatus(boolean status) {
		this.status = status;
	}



	public int getFee() {
		return fee;
	}



	public void setFee(int fee) {
		this.fee = fee;
	}



	public CustomerEntity getCustomer() {
		return customer;
	}



	public void setCustomer(CustomerEntity customer) {
		this.customer = customer;
	}
	
	
	
	

}
