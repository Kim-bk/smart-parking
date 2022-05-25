package com.smartparking.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "customer")
public class CustomerEntity {
	
	@Id
	private String id;
	
	@Field(value = "name")
	private String name;
	
	@Field(value = "number_phone")
	private String numberPhone;
	
	@Field(value = "email")
	private String email;
	
	@Field(value = "customer_card")
	private String customerCard;
	
	private AddressEntity address;

	public CustomerEntity() {
		super();
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getNumberPhone() {
		return numberPhone;
	}

	public void setNumberPhone(String numberPhone) {
		this.numberPhone = numberPhone;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public AddressEntity getAddress() {
		return address;
	}

	public void setAddress(AddressEntity address) {
		this.address = address;
	}

	public String getCustomerCard() {
		return customerCard;
	}

	public void setCustomerCard(String customerCard) {
		this.customerCard = customerCard;
	}

	
	
}
