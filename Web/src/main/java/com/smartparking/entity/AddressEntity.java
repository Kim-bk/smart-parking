package com.smartparking.entity;


import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "address")
public class AddressEntity {
	
	@Id
	private Long id;
	
	@Field(value = "specific_address")
	private String specificAddress;
	
	private ProvinceEntity provinceAddress;
	
	private DistrictEntity districtAddress;
	
	private WardEntity wardAddress;
	
	private CustomerEntity customer;

	public AddressEntity() {
		super();
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getSpecificAddress() {
		return specificAddress;
	}

	public void setSpecificAddress(String specificAddress) {
		this.specificAddress = specificAddress;
	}

	
	public ProvinceEntity getProvinceAddress() {
		return provinceAddress;
	}

	public void setProvinceAddress(ProvinceEntity provinceAddress) {
		this.provinceAddress = provinceAddress;
	}

	public CustomerEntity getCustomer() {
		return customer;
	}

	public void setCustomer(CustomerEntity customer) {
		this.customer = customer;
	}

	public DistrictEntity getDistrictAddress() {
		return districtAddress;
	}

	public void setDistrictAddress(DistrictEntity districtAddress) {
		this.districtAddress = districtAddress;
	}

	public WardEntity getWardAddress() {
		return wardAddress;
	}

	public void setWardAddress(WardEntity wardAddress) {
		this.wardAddress = wardAddress;
	}
	
	
	
	

}
