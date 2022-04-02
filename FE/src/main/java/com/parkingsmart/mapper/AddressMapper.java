package com.parkingsmart.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.parkingsmart.dto.AddressDTO;
import com.parkingsmart.entity.AddressEntity;
import com.parkingsmart.service.impl.DistrictService;
import com.parkingsmart.service.impl.ProvinceService;
import com.parkingsmart.service.impl.WardService;

@Component
public class AddressMapper {
	
	@Autowired
	private ModelMapper mapper;
	
	@Autowired
	private ProvinceService provinceService;
	
	@Autowired
	private ProvinceMapper provinceMapper;
	
	@Autowired
	private DistrictMapper districtMapper;
	
	@Autowired
	private DistrictService districtService;
	
	@Autowired
	private WardMapper wardMapper;
	
	@Autowired
	private WardService wardService;
	
	
	public AddressEntity toEntity(AddressDTO dto) {
		AddressEntity entity = mapper.map(dto, AddressEntity.class);
		entity.setProvinceAddress(provinceMapper.ToEntity(provinceService.findOneById(dto.getIdProvince())));
		entity.setDistrictAddress(districtMapper.toEntity(districtService.findById(dto.getIdDistrict())));
		entity.setWardAddress(wardMapper.toEntity(wardService.findOneById(dto.getIdWard())));
		return entity;
	}
	
	public AddressDTO toDTO(AddressEntity entity) {
		AddressDTO dto = mapper.map(entity, AddressDTO.class);
		dto.setIdProvince(entity.getProvinceAddress().getId());
		dto.setIdDistrict(entity.getDistrictAddress().getId());
		dto.setIdWard(entity.getWardAddress().getId());
		return dto;
	}

}
