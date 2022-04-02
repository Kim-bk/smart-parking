package com.parkingsmart.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToOne;

@Entity(name="address")
public class AddressEntity {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	@Column
	private String specificAddress;
	
	@ManyToOne
	@JoinColumn(name="idProvince")
	private ProvinceEntity provinceAddress;
	
	@ManyToOne
	@JoinColumn(name="idDistrict")
	private DistrictEntity districtAddress;
	
	@ManyToOne
	@JoinColumn(name="idWard")
	private WardEntity wardAddress;
	
	@OneToOne(mappedBy = "address")
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
