package com.smartparking.dto;

import java.util.Date;


public class CustomerParkingDTO {
	
	private String id;
	private String license_plate;
	private Date date_check_in;
	private Date date_check_out;
	private boolean status;	
	private int fee;
	private CustomerDTO customer;
	
	
	public CustomerParkingDTO() {
		super();
	}


	public CustomerParkingDTO(String license_plate, Date date_check_in, Date date_check_out, boolean status, int fee,
			CustomerDTO customer) {
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


	public Date getDate_check_in() {
		return date_check_in;
	}


	public void setDate_check_in(Date date_check_in) {
		this.date_check_in = date_check_in;
	}


	public Date getDate_check_out() {
		return date_check_out;
	}


	public void setDate_check_out(Date date_check_out) {
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


	public CustomerDTO getCustomer() {
		return customer;
	}


	public void setCustomer(CustomerDTO customer) {
		this.customer = customer;
	}


	public String getId() {
		return id;
	}


	public void setId(String id) {
		this.id = id;
	}
	
	
	

}
